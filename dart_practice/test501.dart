void main() {
  var a = "Hello";
  int b = 1;
  double c = 1.0;
  num d = 2;
  d = 2.5;
  var one = int.parse('1');
  var onePointOne = double.parse('1.1');
  String oneAsString = 1.toString();
  String piAsString = 3.14159.toStringAsFixed(2);
  var s3 = 'It\'s easy to escape the string delimiter.';
  var s4 = "It's even easier to use the other delimiter.";
  s4 = "${s3}\n${s4}";
  print(s4);
  bool tf = true;

  int plus1(int number) {
    return number + 1;
  }
  print(plus1(136));

  for (var i = 0; i < 5; i++) {
    print(i);
  }
  var i = 0;
  while (i < 5) {
    print(i);
    i = i + 1;
  }

  void prtf(num number) {
    if (number == 0) {
      print("This is 0");
    }else if (number == 1) {
      print("This is 1");
    } else {
      print("Only 0 or 1");
    }
  }
  void prts(num number) {
    switch (number) {
      case 0:
        print("zero");
      case 1:
        print("one");
      case 2:
        print("two");
      default:
        print("any number");
    }
  }
  for (i = 0; i < 5; i++) {
    prtf(i);
    prts(i);
  }

  try {
    throw "This Is An Error";
  } on IntegerDivisionByZeroException {
    print("OOLE");
  } on Exception catch (e) {
    print("unknown err : $e");
  } catch (e, s) {
    print("unknown unknown err : $e");
    print(s);
  }
}
