Code to analyze events.

### Files
* `lhcbStyle.h`: The usual style options
* `trajectory.h`: Point and Trajectory (adds a direction)
* `data.h`: struct for holding data
* `hits.h`: Hit and Hits, one is a point in space, the other a collection of overlapping phi bins of hits
* `triplet.h`: getTrackPairs, getPDF, Triplet class
* `tracks.h`: Tracks hold triplets
* `utils.h`: FCN, kernel, kernelMax, pvCategory, svCategory
* `plot.c`: Contains plotz, plotxy

You need Pythia installed to generate events, but there is a file there with 10 events with 10 (visible) collisions each to play with. Obviously we’ll need to generate more events, but this is fast (just want to finalize the file format first).

Under the this dir, you can do:

```cpp
.L plot.C
```

then

```cpp
plotz(0); // plot the max kernel value at each z for event 0
plotxy(0,1,val); // plot the 2-d kernel in xy at the z value of pv 1 with shift of val
```

`plotxy(0,1,0)` would draw the 2-d kernel in the x-y plane at the z value of the i=1 pv in the event with index 0.  Doing `plotxy(1,2,0.5)` would draw the same thing for event 1 for its pv with index 2 shifted by +0.5mm in z, etc. I.e., the first argument is the C-style index to the event, the 2nd argument is the C-style index to the PV array for this event, and the z value of that PV is used as the default z value for building the kernel, the last argument lets you shift in z (+ or -) from that default.