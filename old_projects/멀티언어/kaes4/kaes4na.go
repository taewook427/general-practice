package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"encoding/binary"
	"fmt"
	"os"
	"strings"
	"sync"
	"unsafe"

	"golang.org/x/crypto/scrypt"
)

// http://golang.site/go/article/1-Go-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%96%B8%EC%96%B4-%EC%86%8C%EA%B0%9C
// go mod init example.com/test468
// go run test468.go
// go build test468.go
// go build -buildmode=c-shared -o kaes4na.dll

type bytearray struct { // bytearray 구조체
	data []byte // 0 ~ 255
}

func add_byte(b0 *bytearray, b1 *bytearray) *bytearray { // 두 바이트배열을 더해서 새 바이트배열 만들기
	out := bytearray{}
	out.data = make([]byte, len(b0.data)+len(b1.data))
	copy(out.data, b0.data)
	copy(out.data[len(b0.data):], b1.data)
	return &out // 바이트 배열 포인터 반환
}

func read_byte(bytein *bytearray) *string { // 바이트 에레이를 16진법으로 출력
	hex := make([]string, len(bytein.data))
	for i, b := range bytein.data {
		hex[i] = fmt.Sprintf("%02x", b)
	}
	out := strings.Join(hex, " ")
	return &out // 문자열 포인터 반환
}

func (b *bytearray) pad() { // 바이트 배열의 매서드
	padlen := 16 - (len(b.data) % 16)
	for i := 0; i < padlen; i++ {
		b.data = append(b.data, byte(padlen))
	}
} // 16 바이트 패딩

func (b *bytearray) unpad() { // 바이트 배열의 매서드
	padlen := int(b.data[len(b.data)-1])
	b.data = b.data[0 : len(b.data)-padlen]
} // 16 바이트 언패딩

// short encryption no padding, 16B * n
func en1(key *bytearray, iv *bytearray, data *bytearray) *bytearray {
	block, _ := aes.NewCipher(key.data)
	encrypter := cipher.NewCBCEncrypter(block, iv.data)
	var out bytearray
	out.data = make([]byte, len(data.data))
	encrypter.CryptBlocks(out.data, data.data)
	return &out
}

// short decryption no padding, 16B * n
func de1(key *bytearray, iv *bytearray, data *bytearray) *bytearray {
	block, _ := aes.NewCipher(key.data)
	decrypter := cipher.NewCBCDecrypter(block, iv.data)
	var out bytearray
	out.data = make([]byte, len(data.data))
	decrypter.CryptBlocks(out.data, data.data)
	return &out
}

// encryption inline no padding, data 4MB
func en2(keys *[32]bytearray, ivs *[32]bytearray, num int, data *bytearray, out *[32]bytearray, wg *sync.WaitGroup) {
	defer wg.Done() // 고루틴의 완료를 알림
	block, _ := aes.NewCipher(keys[num].data)
	encrypter := cipher.NewCBCEncrypter(block, ivs[num].data)
	var temp bytearray
	temp.data = make([]byte, 131072)
	encrypter.CryptBlocks(temp.data, data.data[131072*num:131072*num+131072])
	out[num] = temp
	ivs[num].data = append([]byte{}, temp.data[131056:131072]...)
}

// decryption inline no padding, data 4MB
func de2(keys *[32]bytearray, ivs *[32]bytearray, num int, data *bytearray, out *[32]bytearray, wg *sync.WaitGroup) {
	defer wg.Done() // 고루틴의 완료를 알림
	block, _ := aes.NewCipher(keys[num].data)
	decrypter := cipher.NewCBCDecrypter(block, ivs[num].data)
	var temp bytearray
	temp.data = make([]byte, 131072)
	decrypter.CryptBlocks(temp.data, data.data[131072*num:131072*num+131072])
	out[num] = temp
	ivs[num].data = append([]byte{}, data.data[131072*num+131056:131072*num+131072]...)
}

func hash(pw *bytearray, salt *bytearray, round int, word int, core int, length int) *bytearray {
	out := bytearray{}
	out.data, _ = scrypt.Key(pw.data, salt.data, round, word, core, length)
	return &out
}

// short encryption no padding 16nB
func enshort(key *bytearray, iv *bytearray, data *bytearray) *bytearray {
	return en1(key, iv, data)
}

// short decryption no padding 16nB
func deshort(key *bytearray, iv *bytearray, data *bytearray) *bytearray {
	return de1(key, iv, data)
}

func enbytes(keychunk *bytearray, data *bytearray) *bytearray {
	keys := [32]bytearray{}
	ivs := [32]bytearray{}
	for i := 0; i < 32; i++ {
		a := bytearray{}
		a.data = keychunk.data[32*i : 32*i+32]
		keys[i] = a
		b := bytearray{}
		b.data = keychunk.data[1024+16*i : 1024+16*i+16]
		ivs[i] = b
	}

	var size int64 = int64(len(data.data))
	num0 := size / 131072
	num1 := size % 131072
	buffer0 := bytearray{}     // input 4MB buffer
	buffer1 := [32]bytearray{} // output 4MB buffer
	var out bytes.Buffer       // output bytes
	var i int64 = 0

	for i = 0; i < num0/32; i++ {
		buffer0.data = data.data[4194304*i : 4194304*i+4194304]
		var wg sync.WaitGroup
		wg.Add(32)
		for j := 0; j < 32; j++ {
			go en2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < 32; j++ {
			out.Write(buffer1[j].data)
		}
	}
	if num0%32 != 0 {
		buffer0.data = data.data[4194304*i : 4194304*i+131072*(num0%32)]
		var wg sync.WaitGroup
		wg.Add(int(num0 % 32))
		for j := 0; j < int(num0%32); j++ {
			go en2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < int(num0%32); j++ {
			out.Write(buffer1[j].data)
		}
	}
	buffer0.data = data.data[size-num1:]
	buffer0.pad()
	out.Write(en1(&keys[num0%32], &ivs[num0%32], &buffer0).data)

	temp := bytearray{}
	temp.data = out.Bytes()
	return &temp
}

func debytes(keychunk *bytearray, data *bytearray) *bytearray {
	keys := [32]bytearray{}
	ivs := [32]bytearray{}
	for i := 0; i < 32; i++ {
		a := bytearray{}
		a.data = keychunk.data[32*i : 32*i+32]
		keys[i] = a
		b := bytearray{}
		b.data = keychunk.data[1024+16*i : 1024+16*i+16]
		ivs[i] = b
	}

	var size int64 = int64(len(data.data))
	num0 := size / 131072
	num1 := size % 131072
	if num1 == 0 {
		num0 = num0 - 1
		num1 = 131072
	}
	buffer0 := bytearray{}     // input 4MB buffer
	buffer1 := [32]bytearray{} // output 4MB buffer
	var out bytes.Buffer       // output bytes
	var i int64 = 0

	for i = 0; i < num0/32; i++ {
		buffer0.data = data.data[4194304*i : 4194304*i+4194304]
		var wg sync.WaitGroup
		wg.Add(32)
		for j := 0; j < 32; j++ {
			go de2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < 32; j++ {
			out.Write(buffer1[j].data)
		}
	}
	if num0%32 != 0 {
		buffer0.data = data.data[4194304*i : 4194304*i+131072*(num0%32)]
		var wg sync.WaitGroup
		wg.Add(int(num0 % 32))
		for j := 0; j < int(num0%32); j++ {
			go de2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < int(num0%32); j++ {
			out.Write(buffer1[j].data)
		}
	}
	buffer0.data = data.data[size-num1:]
	buffer0.data = de1(&keys[num0%32], &ivs[num0%32], &buffer0).data
	buffer0.unpad()
	out.Write(buffer0.data)

	temp := bytearray{}
	temp.data = out.Bytes()
	return &temp
}

func enfile(header *bytearray, keychunk *bytearray, path *string, tgt *string) {
	keys := [32]bytearray{}
	ivs := [32]bytearray{}
	for i := 0; i < 32; i++ {
		a := bytearray{}
		a.data = keychunk.data[32*i : 32*i+32]
		keys[i] = a
		b := bytearray{}
		b.data = keychunk.data[1024+16*i : 1024+16*i+16]
		ivs[i] = b
	}

	f, _ := os.OpenFile(*tgt, os.O_RDWR|os.O_TRUNC|os.O_CREATE, 0666) // write as f
	t, _ := os.Open(*path)                                            // read as t
	defer f.Close()
	defer t.Close()
	f.Write(header.data)
	fileInfo, _ := os.Stat(*path)

	var size int64 = fileInfo.Size()
	num0 := size / 131072
	num1 := size % 131072
	buffer0 := bytearray{}     // input 4MB buffer
	buffer1 := [32]bytearray{} // output 4MB buffer
	var i int64 = 0

	for i = 0; i < num0/32; i++ {
		buffer0.data = make([]byte, 4194304)
		t.Read(buffer0.data)
		var wg sync.WaitGroup
		wg.Add(32)
		for j := 0; j < 32; j++ {
			go en2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < 32; j++ {
			f.Write(buffer1[j].data)
		}
	}
	if num0%32 != 0 {
		buffer0.data = make([]byte, 131072*(num0%32))
		t.Read(buffer0.data)
		var wg sync.WaitGroup
		wg.Add(int(num0 % 32))
		for j := 0; j < int(num0%32); j++ {
			go en2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < int(num0%32); j++ {
			f.Write(buffer1[j].data)
		}
	}
	buffer0.data = make([]byte, num1)
	t.Read(buffer0.data)
	buffer0.pad()
	f.Write(en1(&keys[num0%32], &ivs[num0%32], &buffer0).data)
}

func defile(stpoint int, keychunk *bytearray, path *string, tgt *string) {
	keys := [32]bytearray{}
	ivs := [32]bytearray{}
	for i := 0; i < 32; i++ {
		a := bytearray{}
		a.data = keychunk.data[32*i : 32*i+32]
		keys[i] = a
		b := bytearray{}
		b.data = keychunk.data[1024+16*i : 1024+16*i+16]
		ivs[i] = b
	}

	f, _ := os.OpenFile(*tgt, os.O_RDWR|os.O_TRUNC|os.O_CREATE, 0666) // write as f
	t, _ := os.Open(*path)                                            // read as t
	defer f.Close()
	defer t.Close()
	fileInfo, _ := os.Stat(*path)

	var size int64 = fileInfo.Size() - int64(stpoint)
	num0 := size / 131072
	num1 := size % 131072
	if num1 == 0 {
		num0 = num0 - 1
		num1 = 131072
	}
	buffer0 := bytearray{}     // input 4MB buffer
	buffer1 := [32]bytearray{} // output 4MB buffer

	_, _ = t.Read(make([]byte, stpoint))
	var i int64 = 0

	for i = 0; i < num0/32; i++ {
		buffer0.data = make([]byte, 4194304)
		t.Read(buffer0.data)
		var wg sync.WaitGroup
		wg.Add(32)
		for j := 0; j < 32; j++ {
			go de2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < 32; j++ {
			f.Write(buffer1[j].data)
		}
	}
	if num0%32 != 0 {
		buffer0.data = make([]byte, 131072*(num0%32))
		t.Read(buffer0.data)
		var wg sync.WaitGroup
		wg.Add(int(num0 % 32))
		for j := 0; j < int(num0%32); j++ {
			go de2(&keys, &ivs, j, &buffer0, &buffer1, &wg)
		}
		wg.Wait()
		for j := 0; j < int(num0%32); j++ {
			f.Write(buffer1[j].data)
		}
	}
	buffer0.data = make([]byte, num1)
	t.Read(buffer0.data)
	buffer0.data = de1(&keys[num0%32], &ivs[num0%32], &buffer0).data
	buffer0.unpad()
	f.Write(buffer0.data)
}

func encode(num int) []byte {
	buf := make([]byte, 8)
	binary.LittleEndian.PutUint64(buf, uint64(num))
	return buf
}

//export func0
func func0(arr *C.char) {
	C.free(unsafe.Pointer(arr))
}

//export func1
func func1(pwin *C.char, pwlen C.int, saltin *C.char, saltlen C.int, roundin C.int, wordin C.int, corein C.int, lengthin C.int) *C.char {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice0 := (*[1 << 30]C.char)(unsafe.Pointer(pwin))[:pwlen:pwlen]
	// 바이트 배열로 변환
	pw := make([]byte, len(inslice0))
	for i := 0; i < len(pw); i++ {
		pw[i] = byte(inslice0[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice1 := (*[1 << 30]C.char)(unsafe.Pointer(saltin))[:saltlen:saltlen]
	// 바이트 배열로 변환
	salt := make([]byte, len(inslice1))
	for i := 0; i < len(salt); i++ {
		salt[i] = byte(inslice1[i])
	}

	var round int = int(roundin)
	var word int = int(wordin)
	var core int = int(corein)
	var length int = int(lengthin)
	pw0 := bytearray{}
	pw0.data = pw
	salt0 := bytearray{}
	salt0.data = salt

	temp := hash(&pw0, &salt0, round, word, core, length).data

	olen := len(temp)
	out := make([]C.char, olen)
	for i, p := range temp {
		out[i] = C.char(p)
	}
	// 새로운 C 스타일의 정수 배열 생성
	newArr := (*C.char)(C.malloc(C.size_t(olen) * C.sizeof_char))
	copy((*[1 << 30]C.char)(unsafe.Pointer(newArr))[:olen:olen], out)

	return newArr
}

//export func2
func func2(keyin *C.char, ivin *C.char, datain *C.char, datalen C.int, modein C.int) *C.char {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice0 := (*[1 << 30]C.char)(unsafe.Pointer(keyin))[:32:32]
	// 바이트 배열로 변환
	key := make([]byte, len(inslice0))
	for i := 0; i < len(key); i++ {
		key[i] = byte(inslice0[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice1 := (*[1 << 30]C.char)(unsafe.Pointer(ivin))[:16:16]
	// 바이트 배열로 변환
	iv := make([]byte, len(inslice1))
	for i := 0; i < len(iv); i++ {
		iv[i] = byte(inslice1[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice2 := (*[1 << 30]C.char)(unsafe.Pointer(datain))[:datalen:datalen]
	// 바이트 배열로 변환
	data := make([]byte, len(inslice2))
	for i := 0; i < len(data); i++ {
		data[i] = byte(inslice2[i])
	}

	mode := int(modein)
	key0 := bytearray{}
	key0.data = key
	iv0 := bytearray{}
	iv0.data = iv
	data0 := bytearray{}
	data0.data = data

	var temp []byte
	if mode == 0 { // 0이면 en
		temp = enshort(&key0, &iv0, &data0).data
	} else { // 아니면 de
		temp = deshort(&key0, &iv0, &data0).data
	}
	temp = append(encode(len(temp)), temp...) // temp 길이 8바이트 인코딩 후 더하기

	olen := len(temp)
	out := make([]C.char, olen)
	for i, p := range temp {
		out[i] = C.char(p)
	}
	// 새로운 C 스타일의 정수 배열 생성
	newArr := (*C.char)(C.malloc(C.size_t(olen) * C.sizeof_char))
	copy((*[1 << 30]C.char)(unsafe.Pointer(newArr))[:olen:olen], out)

	return newArr
}

//export func3
func func3(keyin *C.char, datain *C.char, datalen C.int) *C.char {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice0 := (*[1 << 30]C.char)(unsafe.Pointer(keyin))[:1536:1536]
	// 바이트 배열로 변환
	key := make([]byte, len(inslice0))
	for i := 0; i < len(key); i++ {
		key[i] = byte(inslice0[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice1 := (*[1 << 30]C.char)(unsafe.Pointer(datain))[:datalen:datalen]
	// 바이트 배열로 변환
	data := make([]byte, len(inslice1))
	for i := 0; i < len(data); i++ {
		data[i] = byte(inslice1[i])
	}

	key0 := bytearray{}
	key0.data = key
	data0 := bytearray{}
	data0.data = data

	temp := enbytes(&key0, &data0).data
	temp = append(encode(len(temp)), temp...) // temp 길이 8바이트 인코딩 후 더하기

	olen := len(temp)
	out := make([]C.char, olen)
	for i, p := range temp {
		out[i] = C.char(p)
	}
	// 새로운 C 스타일의 정수 배열 생성
	newArr := (*C.char)(C.malloc(C.size_t(olen) * C.sizeof_char))
	copy((*[1 << 30]C.char)(unsafe.Pointer(newArr))[:olen:olen], out)

	return newArr
}

//export func4
func func4(keyin *C.char, datain *C.char, datalen C.int) *C.char {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice0 := (*[1 << 30]C.char)(unsafe.Pointer(keyin))[:1536:1536]
	// 바이트 배열로 변환
	key := make([]byte, len(inslice0))
	for i := 0; i < len(key); i++ {
		key[i] = byte(inslice0[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice1 := (*[1 << 30]C.char)(unsafe.Pointer(datain))[:datalen:datalen]
	// 바이트 배열로 변환
	data := make([]byte, len(inslice1))
	for i := 0; i < len(data); i++ {
		data[i] = byte(inslice1[i])
	}

	key0 := bytearray{}
	key0.data = key
	data0 := bytearray{}
	data0.data = data

	temp := debytes(&key0, &data0).data
	temp = append(encode(len(temp)), temp...) // temp 길이 8바이트 인코딩 후 더하기

	olen := len(temp)
	out := make([]C.char, olen)
	for i, p := range temp {
		out[i] = C.char(p)
	}
	// 새로운 C 스타일의 정수 배열 생성
	newArr := (*C.char)(C.malloc(C.size_t(olen) * C.sizeof_char))
	copy((*[1 << 30]C.char)(unsafe.Pointer(newArr))[:olen:olen], out)

	return newArr
}

//export func5
func func5(headin *C.char, headlen C.int, keyin *C.char, pathin *C.char, pathlen C.int, tgtin *C.char, tgtlen C.int) {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice0 := (*[1 << 30]C.char)(unsafe.Pointer(headin))[:headlen:headlen]
	// 바이트 배열로 변환
	head := make([]byte, len(inslice0))
	for i := 0; i < len(head); i++ {
		head[i] = byte(inslice0[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice1 := (*[1 << 30]C.char)(unsafe.Pointer(keyin))[:1536:1536]
	// 바이트 배열로 변환
	key := make([]byte, len(inslice1))
	for i := 0; i < len(key); i++ {
		key[i] = byte(inslice1[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice2 := (*[1 << 30]C.char)(unsafe.Pointer(pathin))[:pathlen:pathlen]
	// 바이트 배열로 변환
	path := make([]byte, len(inslice2))
	for i := 0; i < len(path); i++ {
		path[i] = byte(inslice2[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice3 := (*[1 << 30]C.char)(unsafe.Pointer(tgtin))[:tgtlen:tgtlen]
	// 바이트 배열로 변환
	tgt := make([]byte, len(inslice3))
	for i := 0; i < len(tgt); i++ {
		tgt[i] = byte(inslice3[i])
	}

	head0 := bytearray{}
	head0.data = head
	key0 := bytearray{}
	key0.data = key
	path0 := string(path)
	tgt0 := string(tgt)

	enfile(&head0, &key0, &path0, &tgt0)
}

//export func6
func func6(stpin C.int, keyin *C.char, pathin *C.char, pathlen C.int, tgtin *C.char, tgtlen C.int) {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice1 := (*[1 << 30]C.char)(unsafe.Pointer(keyin))[:1536:1536]
	// 바이트 배열로 변환
	key := make([]byte, len(inslice1))
	for i := 0; i < len(key); i++ {
		key[i] = byte(inslice1[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice2 := (*[1 << 30]C.char)(unsafe.Pointer(pathin))[:pathlen:pathlen]
	// 바이트 배열로 변환
	path := make([]byte, len(inslice2))
	for i := 0; i < len(path); i++ {
		path[i] = byte(inslice2[i])
	}
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice3 := (*[1 << 30]C.char)(unsafe.Pointer(tgtin))[:tgtlen:tgtlen]
	// 바이트 배열로 변환
	tgt := make([]byte, len(inslice3))
	for i := 0; i < len(tgt); i++ {
		tgt[i] = byte(inslice3[i])
	}

	stpoint0 := int(stpin)
	key0 := bytearray{}
	key0.data = key
	path0 := string(path)
	tgt0 := string(tgt)

	defile(stpoint0, &key0, &path0, &tgt0)
}

func main() {
}
