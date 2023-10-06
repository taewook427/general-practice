package pack1;

public class truck extends pack2.car { // 패키지 2의 car를 상속받음
    truck() {
        System.out.println("패키지 1의 truck 생성자");
    }

    public static void main(String[] args){
        truck tr0 = new truck();
        System.out.println(car.car_name); // 아무것도 안붙임 -> pack1의 car
        System.out.println(pack2.car.car_name); // pack2의 car 변수
    }
}

// ctrl + shift + p -> vscode cmd
// java - create project - no build tool로 프로젝트 생성
// 프로젝트 src 폴더에 폴더를 추가해 패키지 생성
// 패키지 폴더에 java 파일추가, 다른 패키지라서 car.java 중복 가능
// 열때는 java project folder 로 열기