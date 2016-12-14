//LTA Shield Generator
//For the AerE 160 LTA Competition
//Matthew E. Nelson
//Iowa State University

//shield_token STL is available from http://www.thingiverse.com/thing:1050544
//and is licensed under the CC-A-BC

//IR Sensor is from the Sparkfun website at: https://www.sparkfun.com/products/10266

difference(){
scale([2.2,2.2,2.2])
    color([.4,.4,.4])
import("shield_token_v1.stl",convexity=3);
rotate([270,0,248])
translate([-0,-5,-3])
#import("10266.stl",convexity=3);
}