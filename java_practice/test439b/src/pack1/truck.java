package pack1;

import pack2.car; // import pack2.*; 단일 클래스 / 전체 클래스 임포트
// 에제 그냥 car가 pack2.car을 의미

public class truck extends car { // 패키지 2의 car를 상속받음
    truck() {
        System.out.println("패키지 1의 truck 생성자");
    }

    public static void main(String[] args){
        truck tr0 = new truck();
        System.out.println(car.car_name);
        System.out.println(pack2.car.car_name); // 명시 호출 가능
    }
}
