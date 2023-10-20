class person {
  String name = "";
  int age = 0;

  void prt() {
    print("이름 : $name 나이 : $age");
  }
}

class dongsung {
  dongsung() {
    print("DSHS");
  }
}

class yonsei extends dongsung {
  yonsei() {
    print("YonseiUniv");
  }
}

main() {
  var student = person();
  student.name = "bk";
  student.age = 10;
  student.prt();

  var constructor = yonsei();

  List<String> colors = ['Red', 'Orange', 'Yellow'];
  dynamic list2 = [1, 2.5, 'est'];
  list2 = 1;
  var list3 = [0, 1.0];

  print(colors);
  print(list2 + list3[1]);
}
