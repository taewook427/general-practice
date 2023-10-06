package main

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
	"os"
	"strings"
	"sync"

	"golang.org/x/crypto/scrypt"
)

// http://golang.site/go/article/1-Go-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%96%B8%EC%96%B4-%EC%86%8C%EA%B0%9C
// go mod init example.com/test480
// go run test480.go
// go build test480.go
// go build -ldflags -H=windowsgui test480.go

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

func rand_byte(length int) *bytearray { // 난수로 초기화
	out := bytearray{}
	randomBytes := make([]byte, length)
	_, err := rand.Read(randomBytes)
	if err != nil {
		panic(err)
	}
	out.data = randomBytes
	return &out // 바이트 배열 포인터 반환
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

func enwhole(path *string, tgt *string) {
	salt := rand_byte(32)
	ckey := rand_byte(1536)
	mkey := getmkey(salt)
	k0 := bytearray{}
	k0.data = mkey.data[0:32]
	k1 := bytearray{}
	k1.data = mkey.data[32:48]
	ckeydata := en1(&k0, &k1, ckey)

	header := add_byte(salt, ckeydata)
	enfile(header, ckey, path, tgt)
}

func dewhole(path *string, tgt *string) {
	f, _ := os.Open(*path)
	defer f.Close()
	salt := bytearray{}
	salt.data = make([]byte, 32)
	ckeydata := bytearray{}
	ckeydata.data = make([]byte, 1536)
	f.Read(salt.data)
	f.Read(ckeydata.data)

	mkey := getmkey(&salt)
	k0 := bytearray{}
	k0.data = mkey.data[0:32]
	k1 := bytearray{}
	k1.data = mkey.data[32:48]
	ckey := de1(&k0, &k1, &ckeydata)

	defile(1568, ckey, path, tgt)
}

func getmkey(salt *bytearray) *bytearray {
	file, _ := os.Open("key.txt")
	defer file.Close()
	reader := bufio.NewReader(file)
	kfs, _ := reader.ReadString('\n')
	kfs = strings.TrimRight(kfs, "\r\n")
	pws, _ := reader.ReadString('\n')
	pws = strings.TrimRight(pws, "\r\n")

	fileInfo, _ := os.Stat(kfs)
	var size int64 = fileInfo.Size()
	kf := bytearray{}
	kf.data = make([]byte, size)
	f, _ := os.Open(kfs)
	defer f.Close()
	f.Read(kf.data)
	pw := bytearray{}
	pw.data = []byte(pws)

	pw = *add_byte(&pw, &kf)
	mkey := hash(&pw, salt, 16384, 8, 1, 48)
	return mkey
}

func main() {
	folder0, _ := os.Open("enin")
	defer folder0.Close()
	sub0, _ := folder0.ReadDir(-1) // -1은 모든 하위 항목을 읽는 옵션입니다.
	for _, p := range sub0 {
		path := "enin/" + p.Name()
		tgt := "enout/" + p.Name()
		enwhole(&path, &tgt)
		_ = os.Remove(path)
	}

	folder1, _ := os.Open("dein")
	defer folder1.Close()
	sub1, _ := folder1.ReadDir(-1) // -1은 모든 하위 항목을 읽는 옵션입니다.
	for _, p := range sub1 {
		path := "dein/" + p.Name()
		tgt := "deout/" + p.Name()
		dewhole(&path, &tgt)
		_ = os.Remove(path)
	}
}
