//LED Dimensions
led_d=5; //LED Diameter
led_h=8; //LED Height
led_fh=1; //LED FLange Thickness
led_fd=5.5; //LED Flange Diameter
wire_d=.5; //Wire Diameter
wire_h=10; //Wire Height
wire_da=2; // THe distance between the Wires
led();
module led(){
translate([0,0,led_fh])cylinder(led_h-(led_d/2)-led_fh,led_d/2,led_d/2, $fn=25);
translate([0,0,led_h-(led_d/2)])sphere(led_d/2,  $fn=25);
cylinder(led_fh,led_fd/2,led_fd/2, $fn=25);
translate([0,wire_da/2,-wire_h])cylinder(wire_h,wire_d/2,wire_d/2, $fn=25);
translate([0,wire_da/-2,-wire_h])cylinder(wire_h,wire_d/2,wire_d/2, $fn=25);
}