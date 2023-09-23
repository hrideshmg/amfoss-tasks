import 'package:flutter/material.dart';

class StatModel extends ChangeNotifier {
  double? _time;
  double? _distance;

  // Getters allow you to access the value of the property as if they were a variable but its value is computed on the fly
  double? get time => _time;
  double? get distance => _distance;

  void updateValues(time, distance) {
    _time = time;
    _distance = distance;
    notifyListeners();
  }
}
