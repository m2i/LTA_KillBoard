// LTA Laser Cannon
// Matthew E. Nelson
// July 2017
// Revision 1

// Laser canon that can be mounted to servos for use in the AerE 160 LTA
// Laser cannon will hold a 5mm IR LED and support circuit to drive the LED

//Additional licenses and/or code used
/**
 *  Parametric servo arm generator for OpenScad
 *  Générateur de palonnier de servo pour OpenScad
 *
 *  Copyright (c) 2012 Charles Rincheval.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 *  Last update :
 *  https://github.com/hugokernel/OpenSCAD_ServoArms
 *
 *  http://www.digitalspirit.org/
 */

//LED Dimensions in mm
led_d=5; //LED Diameter
led_h=8; //LED Height
led_fh=1; //LED FLange Thickness
led_fd=5.5; //LED Flange Diameter
wire_d=.5; //Wire Diameter
wire_h=10; //Wire Height
wire_da=2; // THe distance between the Wires

//Servo Mount settings

arm_length = 20;

arm_count = 2; // [1,2,3,4,5,6,7,8]

//  Clear between arm head and servo head (PLA: 0.3, ABS 0.2)
SERVO_HEAD_CLEAR = 0.2; // [0.2,0.3,0.4,0.5]

$fn = 40 / 1;

FUTABA_3F_SPLINE = [
    [5.92, 4, 1.1, 2.5],
    [25, 0.3, 0.7, 0.1]
];
//Canon settings
// These are based the focal length for the lens to improve the distance

laser_diameter=36;  //Inner diameter
wall_thickness=5;
laser_length=90;


//-------------------------------------------------------------------
//Draw the cannon

cannon();

// Draw the IR LED and disc.  Disc is movable so it can be focused
translate([0,0,laser_diameter/2])
rotate([90,0,0])
difference() {
cylinder(3,laser_diameter/2-.5,laser_diameter/2-1,$fn=60);
    led();
}

//Draw the IR LED For reference
//rotate([90,0,0])
//translate([0,laser_diameter/2,-1])
//    #led();

//Draw the Servo mount arms



// Modules

module cannon(){
    
    //draws the main body 
    translate([0,0,laser_diameter/2])
    rotate([90,0,0])
    difference() {
        cylinder(laser_length,laser_diameter/2+wall_thickness,laser_diameter/2+wall_thickness,$fn=60);
        translate([0,0,-2]) cylinder(laser_length+5,laser_diameter/2,laser_diameter/2,$fn=60);
    }
    //Draws the servo mount
    rotate([0, 0, 0])
    translate([0,-23,-9.2])
        servo_standard(arm_length, arm_count);
    // Draw the cut-outs for guiding the base unit
    
    
}

module led(){
translate([0,0,led_fh])cylinder(led_h-(led_d/2)-led_fh,led_d/2,led_d/2, $fn=40);
translate([0,0,led_h-(led_d/2)])sphere(led_d/2,  $fn=40);
cylinder(led_fh,led_fd/2,led_fd/2, $fn=40);
translate([0,wire_da/2,-wire_h])cylinder(wire_h,wire_d/2,wire_d/2, $fn=40);
translate([0,wire_da/-2,-wire_h])cylinder(wire_h,wire_d/2,wire_d/2, $fn=40);
}

module servo_futaba_3f(length, count) {
    servo_arm(FUTABA_3F_SPLINE, [length, count]);
}

/**
 *  If you want to support a new servo, juste add a new spline definition array
 *  and a module named like servo_XXX_YYY where XXX is servo brand and YYY is the
 *  connection type (3f) or the servo type (s3003)
 */

module servo_standard(length, count) {
    servo_futaba_3f(length, count);
}

/**
 *  Tooth
 *
 *    |<-w->|
 *    |_____|___
 *    /     \  ^h
 *  _/       \_v
 *   |<--l-->|
 *
 *  - tooth length (l)
 *  - tooth width (w)
 *  - tooth height (h)
 *  - height
 *
 */
module servo_head_tooth(length, width, height, head_height) {
    linear_extrude(height = head_height) {
        polygon([[-length / 2, 0], [-width / 2, height], [width / 2, height], [length / 2,0]]);
    }
}

/**
 *  Servo head
 */
module servo_head(params, clear = SERVO_HEAD_CLEAR) {

    head = params[0];
    tooth = params[1];

    head_diameter = head[0];
    head_heigth = head[1];

    tooth_count = tooth[0];
    tooth_height = tooth[1];
    tooth_length = tooth[2];
    tooth_width = tooth[3];

    % cylinder(r = head_diameter / 2, h = head_heigth + 1);

    cylinder(r = head_diameter / 2 - tooth_height + 0.03 + clear, h = head_heigth);

    for (i = [0 : tooth_count]) {
        rotate([0, 0, i * (360 / tooth_count)]) {
            translate([0, head_diameter / 2 - tooth_height + clear, 0]) {
                servo_head_tooth(tooth_length, tooth_width, tooth_height, head_heigth);
            }
        }
    }
}

/**
 *  Servo hold
 *  - Head / Tooth parameters
 *  - Arms params (length and count)
 */
module servo_arm(params, arms) {

    head = params[0];
    tooth = params[1];

    head_diameter = head[0];
    head_heigth = head[1];
    head_thickness = head[2];
    head_screw_diameter = head[3];

    tooth_length = tooth[2];
    tooth_width = tooth[3];

    arm_length = arms[0];
    arm_count = arms[1];

    /**
     *  Servo arm
     *  - length is from center to last hole
     */
    module arm(tooth_length, tooth_width, head_height, head_heigth, hole_count = 1) {

        arm_screw_diameter = 2;

        difference() {
            union() {
                cylinder(r = tooth_width / 2, h = head_heigth);

                linear_extrude(height = head_heigth) {
                    polygon([
                        [-tooth_width / 2, 0], [-tooth_width / 3, tooth_length],
                        [tooth_width / 3, tooth_length], [tooth_width / 2, 0]
                    ]);
                }

                translate([0, tooth_length, 0]) {
                    cylinder(r = tooth_width / 3, h = head_heigth);
                }

                if (tooth_length >= 12) {
                    translate([-head_heigth / 2 + 2, 3.8, -4]) {
                        rotate([90, 0, 0]) {
                            rotate([0, -90, 0]) {
                                linear_extrude(height = head_heigth) {
                                    polygon([
                                        [-tooth_length / 1.7, 4], [0, 4], [0, - head_height + 5],
                                        [-2, - head_height + 5]
                                    ]);
                                }
                            }
                        }
                    }
                }
            }

            // Hole
            for (i = [0 : hole_count - 1]) {
                //translate([0, length - (length / hole_count * i), -1]) {
                translate([0, tooth_length - (4 * i), -1]) {
                    cylinder(r = arm_screw_diameter / 2, h = 10);
                }
            }

            cylinder(r = head_screw_diameter / 2, h = 10);
        }
    }

    difference() {
        translate([0, 0, 0.1]) {
            cylinder(r = head_diameter / 2 + head_thickness, h = head_heigth + 1);
        }

        cylinder(r = head_screw_diameter / 2, h = 10);

        servo_head(params);
    }

    arm_thickness = head_thickness;

    // Arm
    translate([0, 0, head_heigth]) {
        for (i = [0 : arm_count - 1]) {
            rotate([0, 0, i * (360 / arm_count)]) {
                arm(arm_length, head_diameter + arm_thickness * 2, head_heigth, 2);
            }
        }
    }
}