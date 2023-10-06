package main

import (
	"fmt"
	"os"
	"os/exec"
)

// http://golang.site/go/article/1-Go-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%96%B8%EC%96%B4-%EC%86%8C%EA%B0%9C
// go mod init example.com/test484
// go run test484.go
// go build test484.go

func main() {
	fmt.Println("kcom4man 실행 보조기\n0 : kcl4relay, 1 : kcom4ssh, 2 : kcom4gui")
	var num int
	_, _ = fmt.Scanf("%d\n", &num)

	out := ""
	switch num {
	case 0:
		out = "kcl4relay"
	case 1:
		out = "kcom4ssh"
	case 2:
		out = "kcom4gui"
	}

	out = "[order]{[name]{\"" + out + "\"}}"
	fmt.Println(out)
	f, _ := os.Create("enin/manager.txt")
	f.Write([]byte(out))
	f.Close()

	cmd := exec.Command("./test480")
	// 명령 실행 및 결과 처리
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("오류:", err)
		return
	}
	// 실행 결과 출력
	fmt.Println(string(output))

	fmt.Println("Press Enter To Exit...")
	var end int
	_, _ = fmt.Scanf("%s\n", &end)
}
