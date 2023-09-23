import 'package:flutter/material.dart';
import 'package:flutter_osm_plugin/flutter_osm_plugin.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:provider/provider.dart';
import 'package:geoquest/stats_model.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => StatModel()),
        Provider<MapController>(create: (context) {
          return MapController(
              initMapWithUserPosition: const UserTrackingOption());
        }),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'GeoQuest',
      home: MapScreen(),
    );
  }
}

// In flutter the state of the app is separate from the widget
class MapScreen extends StatefulWidget {
  const MapScreen({super.key});
  // createState is a is a method that returns an instance of a state class (MapScreenState() in this case)
  // MapScreenState before createState specifies the return type of createState (similar to using void)
  @override
  MapScreenState createState() => MapScreenState();
}

class MapScreenState extends State<MapScreen> with OSMMixinObserver {
  late MapController mapController;
  late GeoPoint initPosition;

  // Saves and displays the users current position
  @override
  Future<void> mapIsReady(bool isReady) async {
    if (isReady) {
      initPosition = await mapController.myLocation();
      mapController.addMarker(initPosition,
          markerIcon: const MarkerIcon(
              icon: Icon(Icons.location_on, color: Colors.green)));
    }
  }

  @override
  Widget build(BuildContext context) {
    mapController = Provider.of<MapController>(context);
    mapController.addObserver(this);
    StatModel stats = Provider.of(context,
        listen: false); // listen needs to be false prevent rebuilding

    mapController.listenerMapSingleTapping.addListener(() async {
      if (mapController.listenerMapSingleTapping.value != null) {
        mapController.removeLastRoad();
        GeoPoint destPosition = mapController.listenerMapSingleTapping
            .value!; // the ! assures that the value will never be null
        RoadInfo journey = await mapController.drawRoad(
            initPosition, destPosition,
            roadOption:
                const RoadOption(roadColor: Colors.green, zoomInto: true));

        stats.updateValues(journey.duration, journey.distance);
      }
    });

    return Scaffold(
      appBar: AppBar(
        title: const Text(
            style: TextStyle(fontWeight: FontWeight.bold), 'GeoQuest'),
        centerTitle: true,
        backgroundColor: Colors.green,
      ),
      body: Column(
        children: [
          Expanded(
            child: OSMFlutter(
                controller: mapController,
                osmOption: const OSMOption(
                  zoomOption: ZoomOption(initZoom: 12),
                ),
                mapIsLoading: const SpinKitFadingCube(color: Colors.green)),
          ),
          const BottomBar()
        ],
      ),
    );
  }
}

class BottomBar extends StatelessWidget {
  const BottomBar({super.key});

  @override
  Widget build(BuildContext context) {
    final stats = Provider.of<StatModel>(context);
    final MapController mapController = Provider.of<MapController>(context);

    if (stats.time != null && stats.distance != null) {
      final hours = stats.time! ~/ 3600;
      final mins = (stats.time! % 3600) ~/ 60;
      const TextStyle headingStyle = TextStyle(
          color: Colors.white, fontSize: 23, fontWeight: FontWeight.w600);
      const TextStyle statStyle = TextStyle(color: Colors.white, fontSize: 20);

      return Container(
        color: Colors.green,
        height: 75,
        child: Stack(
            alignment: Alignment.center,
            clipBehavior: Clip.none,
            children: [
              Positioned(
                  top: -30,
                  child: IconButton(
                      icon: const Icon(Icons.cancel_rounded),
                      color: Colors.white,
                      iconSize: 85,
                      onPressed: () {
                        mapController.removeLastRoad();
                        stats.updateValues(null, null);
                      })),
              Positioned(
                  top: 10,
                  child: Row(children: [
                    Padding(
                      padding: const EdgeInsets.only(left: 40),
                      child: Column(
                        children: [
                          const Text(style: headingStyle, "Time"),
                          Text(style: statStyle, "$hours:$mins Hours")
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(right: 10, left: 165),
                      child: Column(
                        children: [
                          const Text(style: headingStyle, "Distance"),
                          Text(
                              style: statStyle,
                              "${stats.distance!.toStringAsFixed(2)} km")
                        ],
                      ),
                    )
                  ]))
            ]),
      );
    } else {
      return Container(
        height: 75,
        color: Colors.green,
        alignment: Alignment.center,
        child: const Text(
            style: TextStyle(
                fontSize: 26, color: Colors.white, fontWeight: FontWeight.w600),
            "Tap to place your marker!"),
      );
    }
  }
}
