package main

import (
	"fmt"
	"os"
	"os/user"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"

	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"

	noncryptrand "math/rand"

	"unsafe"

	"golang.org/x/crypto/sha3"
)

/*
#include <stdlib.h>
*/
import "C"

type bytearray struct { // bytearray 구조체
	data []byte // 0 ~ 255
}

func init_byte(length int) *bytearray { // 0으로 초기화
	out := bytearray{}
	out.data = make([]byte, length)
	return &out // 바이트 배열 포인터 반환
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

func from_string(strin *string) *bytearray { // 문자열에서 utf-8 인코딩
	out := bytearray{}
	out.data = []byte(*strin)
	return &out // 바이트 배열 포인터 반환
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

func (b *bytearray) equals(tgt *bytearray) bool { // 두 바이트배열의 동일성 확인
	if len(b.data) != len(tgt.data) {
		return false
	} else {
		for i, p := range b.data {
			if p != tgt.data[i] {
				return false
			}
		}
		return true
	}
}

func delete(target string, mode int) { // target : file path, mode : int
	fileInfo, err1 := os.Stat(target)
	if err1 != nil {
		panic(err1)
	}
	var size int64 = fileInfo.Size() // file size
	file, err0 := os.OpenFile(target, os.O_RDWR|os.O_TRUNC, 0666)
	if err0 != nil {
		panic(err0)
	}

	if mode == 0 { // normal delete
		var num0 int64 = size / 1048576
		var num1 int = int(size % 1048576)

		temp := *init_byte(1048576)
		for i := num0; i > 0; i-- {
			_, _ = file.Write(temp.data)
		}

		temp = *init_byte(num1)
		_, _ = file.Write(temp.data)

	} else { // secure delete
		var num0 int64 = size / 1024
		var num1 int = int(size % 1024)

		for i := num0 / 100; i > 0; i-- {
			temp := *rand_byte(1024)
			for j := 0; j < 100; j++ {
				_, _ = file.Write(temp.data)
			}
		}

		temp := *rand_byte(1024)
		for i := num0 % 100; i > 0; i-- {
			_, _ = file.Write(temp.data)
		}

		temp = *rand_byte(num1)
		file.Write(temp.data)
	}

	file.Close()
	_ = os.Remove(target)
}

// files -> tempkaesl
func dozip(targets *[]string) {
	num := len(*targets)
	file, err0 := os.OpenFile("tempkaesl", os.O_RDWR|os.O_TRUNC|os.O_CREATE, 0666)
	if err0 != nil {
		panic(err0)
	}
	_, _ = file.Write([]byte{byte(num % 256), byte(num / 256)})

	for _, fname := range *targets {
		tempname := strings.Replace(fname, "\\", "/", -1)
		lastIndex := strings.LastIndex(tempname, "/")
		tempname = tempname[lastIndex+1:]
		namebyte := *from_string(&tempname) // file name
		namelen := len(namebyte.data)       // file name size
		_, _ = file.Write([]byte{byte(namelen % 256), byte(namelen / 256)})
		_, _ = file.Write(namebyte.data)

		fileInfo, _ := os.Stat(fname)
		var size int64 = fileInfo.Size() // file size
		tempsize := size
		tempbyte := make([]byte, 8)
		for i := 0; i < 8; i++ {
			tempbyte[i] = byte(tempsize % 256)
			tempsize = tempsize / 256
		}
		_, _ = file.Write(tempbyte)

		var num0 int64 = size / 1048576
		var num1 int = int(size % 1048576)
		t, _ := os.Open(fname)
		buffer := make([]byte, 1048576)
		for i := num0; i > 0; i-- {
			t.Read(buffer)
			file.Write(buffer)
		}
		buffer = make([]byte, num1)
		t.Read(buffer)
		file.Write(buffer)
		t.Close()
	}

	file.Close()
}

// tempkaesl -> path + files
func unzip(path string) { // path : folder path
	path = strings.Replace(path, "\\", "/", -1)
	if path == "" {
		path = "./"
	} else if path[len(path)-1:] != "/" {
		path = path + "/"
	}

	file, _ := os.Open("tempkaesl")
	buffer := make([]byte, 2)
	file.Read(buffer)
	var num int = int(buffer[0]) + int(buffer[1])*256

	for i := 0; i < num; i++ {
		buffer = make([]byte, 2)
		file.Read(buffer)
		var namelen int = int(buffer[0]) + int(buffer[1])*256
		buffer = make([]byte, namelen)
		file.Read(buffer)
		namestr := string(buffer)

		var filesize int64 = 0
		var multi int64 = 1
		buffer = make([]byte, 8)
		file.Read(buffer)
		for j := 0; j < 8; j++ {
			filesize = filesize + int64(buffer[j])*multi
			if j != 7 {
				multi = multi * 256
			}
		}

		var num0 int64 = filesize / 1048576
		var num1 int = int(filesize % 1048576)
		t, _ := os.OpenFile(path+namestr, os.O_RDWR|os.O_TRUNC|os.O_CREATE, 0666)
		buffer = make([]byte, 1048576)
		for j := num0; j > 0; j-- {
			file.Read(buffer)
			t.Write(buffer)
		}
		buffer = make([]byte, num1)
		file.Read(buffer)
		t.Write(buffer)
		t.Close()
	}

	file.Close()
}

// key expand inline
func inline0(ckey *bytearray, num int, keys *[32]bytearray, wg *sync.WaitGroup) {
	defer wg.Done()        // 고루틴의 완료를 알림
	temp := (7 * num) % 16 // round st point
	var pre, sub bytearray
	if temp > 8 {
		pre.data = append([]byte{}, ckey.data[8*temp-64:8*temp]...)
		sub.data = append([]byte{}, ckey.data[8*temp:]...)
		sub.data = append(sub.data, ckey.data[:8*temp-64]...)
	} else {
		pre.data = append([]byte{}, ckey.data[8*temp+64:]...)
		pre.data = append(pre.data, ckey.data[:8*temp]...)
		sub.data = append([]byte{}, ckey.data[8*temp:8*temp+64]...)
	}
	for i := 0; i < 10000; i++ {
		sub.data = append(pre.data, sub.data...)
		temp := sha3.Sum256(sub.data)
		sub.data = temp[:]
	}
	keys[num].data = sub.data[0:16]
	keys[num+16].data = sub.data[16:32]
}

// key expand function
func expandkey(ckey *bytearray) *[32]bytearray {
	var out [32]bytearray
	var wg sync.WaitGroup
	wg.Add(16)
	for i := 0; i < 16; i++ {
		go inline0(ckey, i, &out, &wg)
	}
	wg.Wait()
	return &out
}

// short encryption no padding, data 4MB
func inline1(keys *[32]bytearray, ivs *[32]bytearray, num int, data *bytearray, out *[32]bytearray, wg *sync.WaitGroup) {
	defer wg.Done() // 고루틴의 완료를 알림
	block, _ := aes.NewCipher(keys[num].data)
	encrypter := cipher.NewCBCEncrypter(block, ivs[num].data)
	var temp bytearray
	temp.data = make([]byte, 131072)
	encrypter.CryptBlocks(temp.data, data.data[131072*num:131072*num+131072])
	out[num] = temp
	ivs[num].data = append([]byte{}, temp.data[131056:131072]...)
}

// short encryption no padding, 16B * n
func inline1t(key *bytearray, iv *bytearray, data *bytearray) *bytearray {
	block, _ := aes.NewCipher(key.data)
	encrypter := cipher.NewCBCEncrypter(block, iv.data)
	var out bytearray
	out.data = make([]byte, len(data.data))
	encrypter.CryptBlocks(out.data, data.data)
	return &out
}

// encrypt(tempkaesl) -> move to path, 32 process
func encrypt(hint *string, pw *string, path *string) { // hint *str, pw *str, file path *str
	salt := *rand_byte(32)  // salt bytearray
	ckey := *rand_byte(128) // content key bytearray
	iv := *rand_byte(16)    // iv bytearray
	pwbyte := []byte(*pw)   // pw byte

	var pwhash bytearray // pwh bytearray
	pwhash.data = append([]byte{}, pwbyte...)
	for i := 0; i < 100000; i++ {
		pwhash.data = append(salt.data, pwhash.data...)
		temp := sha3.Sum256(pwhash.data)
		pwhash.data = temp[:]
	}
	var mkey bytearray // masterkey bytearray
	mkey.data = append([]byte{}, pwbyte...)
	for i := 0; i < 10000; i++ {
		mkey.data = append(mkey.data, salt.data...)
		temp := sha3.Sum256(mkey.data)
		mkey.data = temp[:]
	}

	hintbyte := []byte(*hint) // hint byte
	hintsize := len(hintbyte) // hint size
	var enckey bytearray
	var enciv bytearray
	enckey.data = mkey.data[16:32]
	enciv.data = mkey.data[0:16]
	ckeydata := inline1t(&enckey, &enciv, &ckey)

	var header bytearray // header bytearray
	header.data = []byte("OTE1")
	header.data = append(header.data, []byte{byte(hintsize % 256), byte(hintsize / 256)}...)
	header.data = append(header.data, hintbyte...)
	header.data = append(header.data, salt.data...)
	header.data = append(header.data, pwhash.data...)
	header.data = append(header.data, ckeydata.data...)
	header.data = append(header.data, iv.data...)

	keys := expandkey(&ckey) // 16B * 32 keys bytearray[]
	var ivs [32]bytearray    // 16B * 32 ivs bytearray[]
	for i := 0; i < 32; i++ {
		ivs[i] = iv
	}
	fileInfo, _ := os.Stat("./tempkaesl")
	var size int64 = fileInfo.Size() // file size
	chunknum0 := size / 131072       // chunk num
	chunknum1 := size % 131072       // left size

	f, _ := os.OpenFile(*path, os.O_RDWR|os.O_TRUNC|os.O_CREATE, 0666) // write as f
	t, _ := os.Open("tempkaesl")                                       // read as t
	defer f.Close()
	defer t.Close()

	f.Write(header.data)
	towrite := [32]bytearray{}

	for i := chunknum0 / 32; i > 0; i-- {
		var buffer bytearray
		buffer.data = make([]byte, 4194304)
		t.Read(buffer.data)

		var wg sync.WaitGroup
		wg.Add(32)
		for j := 0; j < 32; j++ {
			go inline1(keys, &ivs, j, &buffer, &towrite, &wg)
		}
		wg.Wait()

		for j := 0; j < 32; j++ {
			f.Write(towrite[j].data)
		}
	}

	if chunknum0%32 != 0 {
		var buffer bytearray
		buffer.data = make([]byte, 131072*(chunknum0%32))
		t.Read(buffer.data)

		var wg sync.WaitGroup
		wg.Add(int(chunknum0 % 32))
		for i := 0; i < int(chunknum0%32); i++ {
			go inline1(keys, &ivs, i, &buffer, &towrite, &wg)
		}
		wg.Wait()
	}
	for i := 0; i < int(chunknum0%32); i++ {
		f.Write(towrite[i].data)
	}

	var buffer bytearray
	buffer.data = make([]byte, chunknum1)
	if chunknum1 != 0 {
		t.Read(buffer.data)
	} else {
		buffer.data = make([]byte, 0)
	}
	buffer.pad()
	count := int(chunknum0 % 32)
	temp := inline1t(&keys[count], &ivs[count], &buffer)
	f.Write(temp.data)
}

// short decryption no padding, data 4MB
func inline2(keys *[32]bytearray, ivs *[32]bytearray, num int, data *bytearray, out *[32]bytearray, wg *sync.WaitGroup) {
	defer wg.Done() // 고루틴의 완료를 알림
	block, _ := aes.NewCipher(keys[num].data)
	decrypter := cipher.NewCBCDecrypter(block, ivs[num].data)
	var temp bytearray
	temp.data = make([]byte, 131072)
	decrypter.CryptBlocks(temp.data, data.data[131072*num:131072*num+131072])
	out[num] = temp
	ivs[num].data = append([]byte{}, data.data[131072*num+131056:131072*num+131072]...)
}

// short decryption no padding, 16B * n
func inline2t(key *bytearray, iv *bytearray, data *bytearray) *bytearray {
	block, _ := aes.NewCipher(key.data)
	decrypter := cipher.NewCBCDecrypter(block, iv.data)
	var out bytearray
	out.data = make([]byte, len(data.data))
	decrypter.CryptBlocks(out.data, data.data)
	return &out
}

// decrypt(path) -> tempkaesl, 32 process
func decrypt(target *string, pw *string) { // target path *str, pw *str
	f, _ := os.Open(*target)                                                 // read as f
	t, _ := os.OpenFile("tempkaesl", os.O_RDWR|os.O_TRUNC|os.O_CREATE, 0666) // write as t
	defer f.Close()
	defer t.Close()

	var buffer bytearray
	buffer.data = make([]byte, 4)
	f.Read(buffer.data)
	buffer.data = make([]byte, 2)
	f.Read(buffer.data)
	hintnum := int(buffer.data[0]) + 256*int(buffer.data[1])
	buffer.data = make([]byte, hintnum)
	f.Read(buffer.data)
	var saltbyte bytearray // salt bytearray 32B
	saltbyte.data = make([]byte, 32)
	f.Read(saltbyte.data)
	var pwhash bytearray // pwhash bytearray 32B
	pwhash.data = make([]byte, 32)
	f.Read(pwhash.data)
	var ckeydata bytearray // ckeydata bytearray 128B
	ckeydata.data = make([]byte, 128)
	f.Read(ckeydata.data)
	var iv bytearray // iv bytearray 16B
	iv.data = make([]byte, 16)
	f.Read(iv.data)

	var mkey bytearray // masterkey bytearray
	mkey.data = append([]byte{}, []byte(*pw)...)
	for i := 0; i < 10000; i++ {
		mkey.data = append(mkey.data, saltbyte.data...)
		temp := sha3.Sum256(mkey.data)
		mkey.data = temp[:]
	}

	var enckey bytearray
	var enciv bytearray
	enckey.data = mkey.data[16:32]
	enciv.data = mkey.data[0:16]
	ckey := inline2t(&enckey, &enciv, &ckeydata) // content key *bytearray

	keys := expandkey(ckey) // 16B * 32 keys bytearray[]
	var ivs [32]bytearray   // 16B * 32 ivs bytearray[]
	for i := 0; i < 32; i++ {
		ivs[i] = iv
	}
	fileInfo, _ := os.Stat(*target)
	var size int64 = fileInfo.Size() - int64(hintnum+214) // actual file size
	chunknum0 := size / 131072                            // chunk num
	chunknum1 := size % 131072                            // left size
	if chunknum1 == 0 {
		chunknum0 = chunknum0 - 1
		chunknum1 = 131072
	}

	towrite := [32]bytearray{}
	for i := chunknum0 / 32; i > 0; i-- {
		var buffer bytearray
		buffer.data = make([]byte, 4194304)
		f.Read(buffer.data)

		var wg sync.WaitGroup
		wg.Add(32)
		for j := 0; j < 32; j++ {
			go inline2(keys, &ivs, j, &buffer, &towrite, &wg)
		}
		wg.Wait()

		for j := 0; j < 32; j++ {
			t.Write(towrite[j].data)
		}
	}

	if chunknum0%32 != 0 {
		var buffer bytearray
		buffer.data = make([]byte, 131072*(chunknum0%32))
		f.Read(buffer.data)

		var wg sync.WaitGroup
		wg.Add(int(chunknum0 % 32))
		for i := 0; i < int(chunknum0%32); i++ {
			go inline2(keys, &ivs, i, &buffer, &towrite, &wg)
		}
		wg.Wait()
	}
	for i := 0; i < int(chunknum0%32); i++ {
		t.Write(towrite[i].data)
	}

	buffer.data = make([]byte, chunknum1)
	f.Read(buffer.data)
	count := int(chunknum0 % 32)
	temp := inline2t(&keys[count], &ivs[count], &buffer)
	temp.unpad()
	t.Write(temp.data)
}

// valid pw check
func check(salt *bytearray, pw *string, pwhash *bytearray) bool { // salt : *bytearray, pw : *str, pwhash : *bytearray
	var chk bytearray // pwh check bytearray
	chk.data = append([]byte{}, []byte(*pw)...)
	for i := 0; i < 100000; i++ {
		chk.data = append(salt.data, chk.data...)
		temp := sha3.Sum256(chk.data)
		chk.data = temp[:]
	}
	return pwhash.equals(&chk)
}

// valid file check, get pwhs
func view(target *string) *[4]bytearray { // target : file path
	var out [4]bytearray
	f, _ := os.Open(*target) // read as f
	defer f.Close()
	var buffer bytearray
	buffer.data = make([]byte, 4)
	f.Read(buffer.data)
	var chk bytearray
	chk.data = []byte{79, 84, 69, 49}

	if buffer.equals(&chk) {
		var b0 bytearray
		b0.data = []byte{0}
		out[0] = b0

		buffer.data = make([]byte, 2)
		f.Read(buffer.data)
		hintnum := int(buffer.data[0]) + 256*int(buffer.data[1])
		var b1 bytearray
		b1.data = make([]byte, hintnum)
		f.Read(b1.data)
		out[1] = b1

		var b2 bytearray // salt bytearray 32B
		b2.data = make([]byte, 32)
		f.Read(b2.data)
		out[2] = b2

		var b3 bytearray // pwhash bytearray 32B
		b3.data = make([]byte, 32)
		f.Read(b3.data)
		out[3] = b3

	} else {
		var b0 bytearray
		b0.data = []byte{1}
		out[0] = b0
	}

	return &out
}

// mode : 0 del 1 non del, 0 normal 5 secure
func mainengine(enfiles *[]string, defile *string, hint *string, pws *[2]string, mode int) *string {
	out := "complete"
	currentUser, _ := user.Current()
	desktopPath := filepath.Join(currentUser.HomeDir, "Desktop")
	outpath := desktopPath + "/" // 출력 경로
	delmode := mode / 5
	var isdel bool
	if mode%2 == 0 {
		isdel = true
	} else {
		isdel = false
	}

	if len(*enfiles) != 0 {
		if pws[0] == pws[1] {
			noncryptrand.Seed(time.Now().UnixNano())
			name := "kaesl" + fmt.Sprint(1000+noncryptrand.Intn(9000)) + ".ote"
			nm := outpath + name
			dozip(enfiles)
			encrypt(hint, &pws[0], &nm)
			delete("./tempkaesl", delmode)
			if isdel {
				for _, p := range *enfiles {
					delete(p, delmode)
				}
			}
			out = "complete : " + name
		} else {
			out = "complete : PW not match"
		}
	} else if *defile != "" {
		info := view(defile)
		if info[0].data[0] == 0 {
			if check(&info[2], &pws[0], &info[3]) {
				decrypt(defile, &pws[0])
				noncryptrand.Seed(time.Now().UnixNano())
				name := "kaesl" + fmt.Sprint(1000+noncryptrand.Intn(9000)) + "/"
				nm := outpath + name
				_, err := os.Stat(nm)
				if os.IsNotExist(err) {
					os.MkdirAll(nm, 0755)
				}
				unzip(nm) // 새 폴더가 생성됨 주의
				delete("./tempkaesl", delmode)
				if isdel {
					delete(*defile, delmode)
				}
				out = "complete : " + name
			} else {
				out = "complete : Not Valid PW"
			}
		} else {
			out = "complete : Not Valid OTE"
		}
	} else {
		out = "complete : Nothing"
	}

	r := recover()
	if r != nil {
		out = fmt.Sprint(r)
	}
	return &out
}

//export engine
func engine(arr0 *C.char, length0 C.int) *C.char {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice := (*[1 << 30]C.char)(unsafe.Pointer(arr0))[:length0:length0]

	// 바이트 배열로 변환
	ordslice := make([]byte, len(inslice))
	for i := 0; i < len(ordslice); i++ {
		ordslice[i] = byte(inslice[i])
	}

	/*
		글자수는 utf-8 인코딩 시 기준
		3글자 : enfiles 개수
		(3글자 + n글자) * n : enfiles 요소
		3글자 : defile 길이
		n글자 : defile
		3글자 : hint 길이
		n글자 : hint
		3글자 : pw0 길이
		n글자 : pw0
		3글자 : pw1 길이
		n글자 : pw1
		1글자 : mode
	*/
	order := string(ordslice)
	count := 0

	temp, _ := strconv.ParseInt(order[count:count+3], 10, 64)
	count = count + 3
	enfiles := make([]string, temp)
	for i := temp; i > 0; i-- {
		tlen, _ := strconv.ParseInt(order[count:count+3], 10, 64)
		count = count + 3
		enfiles[i-1] = order[count : count+int(tlen)]
		count = count + int(tlen)
	}

	temp, _ = strconv.ParseInt(order[count:count+3], 10, 64)
	count = count + 3
	defile := ""
	if temp != 0 {
		defile = order[count : count+int(temp)]
	}
	count = count + int(temp)

	temp, _ = strconv.ParseInt(order[count:count+3], 10, 64)
	count = count + 3
	hint := ""
	if temp != 0 {
		hint = order[count : count+int(temp)]
	}
	count = count + int(temp)

	temp, _ = strconv.ParseInt(order[count:count+3], 10, 64)
	count = count + 3
	pw0 := ""
	if temp != 0 {
		pw0 = order[count : count+int(temp)]
	}
	count = count + int(temp)

	temp, _ = strconv.ParseInt(order[count:count+3], 10, 64)
	count = count + 3
	pw1 := ""
	if temp != 0 {
		pw1 = order[count : count+int(temp)]
	}
	count = count + int(temp)

	mt, _ := strconv.ParseInt(order[count:count+1], 10, 64)
	mode := int(mt)

	pws := [2]string{pw0, pw1}
	output := *mainengine(&enfiles, &defile, &hint, &pws, mode) // 길이(1) + 반환 바이트(n)
	r := recover()
	if r != nil {
		output = fmt.Sprint(r)
	}
	if len(output) > 255 {
		output = output[0:255]
	}

	outbyte := append([]byte{byte(len(output))}, []byte(output)...)
	length := len(outbyte)
	tempbyte := make([]C.char, length)
	for i, p := range outbyte {
		tempbyte[i] = C.char(p)
	}

	// 새로운 C 스타일의 정수 배열 생성
	newArr := (*C.char)(C.malloc(C.size_t(length) * C.sizeof_char))
	copy((*[1 << 30]C.char)(unsafe.Pointer(newArr))[:length:length], tempbyte)

	return newArr
}

//export seehint
func seehint(arr0 *C.char, length0 C.int) *C.char {
	// C 스타일의 정수 배열을 Go 슬라이스로 변환
	inslice := (*[1 << 30]C.char)(unsafe.Pointer(arr0))[:length0:length0]

	// 바이트 배열로 변환
	ordslice := make([]byte, len(inslice))
	for i := 0; i < len(ordslice); i++ {
		ordslice[i] = byte(inslice[i])
	}

	/*
		글자수는 utf-8 기준
		3글자 : 파일명 길이
		n글자 : 파일 이름
	*/
	order := string(ordslice)
	temp, _ := strconv.ParseInt(order[0:3], 10, 64)
	name := order[3 : 3+int(temp)]

	b4 := view(&name)
	output := ""
	if b4[0].data[0] == 0 {
		output = string(b4[1].data)
	} else {
		output = "Warning : Not Valid OTE File"
	}
	r := recover()
	if r != nil {
		output = fmt.Sprint(r)
	}
	if len(output) > 255 {
		output = output[0:255]
	}

	outbyte := append([]byte{byte(len(output))}, []byte(output)...)
	length := len(outbyte)
	tempbyte := make([]C.char, length)
	for i, p := range outbyte {
		tempbyte[i] = C.char(p)
	}

	// 새로운 C 스타일의 정수 배열 생성
	newArr := (*C.char)(C.malloc(C.size_t(length) * C.sizeof_char))
	copy((*[1 << 30]C.char)(unsafe.Pointer(newArr))[:length:length], tempbyte)

	return newArr
}

//export freeptr
func freeptr(arr *C.char) {
	C.free(unsafe.Pointer(arr))
}

func main() {
}

// http://golang.site/go/article/1-Go-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%96%B8%EC%96%B4-%EC%86%8C%EA%B0%9C
// go mod init example.com/test376
// go run test376.go
// go build test376.go
// go build -buildmode=c-shared -o mydll.dll
