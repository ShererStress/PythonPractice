import tkinter as tk;
import math;

x_dim = 10;
y_dim = 10;
box_size = 40;

#objects

class Unit:

    def __init__(self, team_in, unit_data, x_in, y_in):
        self.team_id = team_in;
        self.movespeed = unit_data;
        self.x_pos = x_in;
        self.y_pos = y_in;
        self.awaiting_orders = True;
        selected_tile = x_in+10*y_in;
        map_tile_list[selected_tile].assign_unit(self);

    def display_location():
        print(f"{self.x_pos} - {self.y_pos}");

    def complete_orders(self):
        print("This unit has completed it's turn");
        self.awaiting_orders = False;

    def attack_target(self, target_unit, allow_counterattack = False):
        if allow_counterattack:
            print("ATTACKING");
            target_unit.attack_target(self);
        else:
            print("DEFENDING");

# Inf, Rocket Inf, Light Supply, Light Art, AT Gun
# Light Transport, Decoy Platform, GtA Missile, Seeker Platform
# Light Tank, AA, Armored Supply, Heavy Tank, Self-Prop Art
# Recon, Flanker, Tank-Killer
# --
# Jump Jet, Assault Inf
# EM Disruptor, Rocket
# Adv tank
# Air-Killer, Mimic

class MapTile:

    def __init__(self, rectange_id, x_pos_in, y_pos_in, move_cost_in = 1):
        self.canvas_rect_id = rectange_id;
        self.occupied = False;
        self.occupying_unit = None;
        self.x_pos = x_pos_in;
        self.y_pos = y_pos_in;
        self.move_cost = move_cost_in;

    def update_display(self, override=0):
        selected_color="red";
        if(self.occupied == True):
            if(self.occupying_unit.team_id==0):
                selected_color = "green";
            else:
                selected_color = "yellow";
        else:
            selected_color = "black";
        map_area.itemconfig(self.canvas_rect_id, fill=selected_color);

    def assign_unit(self, unit_in):
        self.occupied = True;
        self.occupying_unit = unit_in;
        self.update_display();

    def unassign_unit(self):
        self.occupied = False;
        self.occupying_unit = None;
        self.update_display();


class GameLogic:

    def __init__(self):
        self.active_movement_tile = None;
        self.active_combat_tile = None;
        self.valid_target_tiles = [];
        self.overlay_tile_ids = [];

    def handle_click(self, selected_tile):
        if self.active_movement_tile == None:
            if selected_tile.occupied:
                if selected_tile.occupying_unit.awaiting_orders == False:
                    print("That unit has already moved, but that's ok for now");
                self.activate_unit(selected_tile);
            else:
                print("Nothing here");
        else:
            if self.active_combat_tile == None:
                x_diff = abs(self.active_movement_tile.x_pos-selected_tile.x_pos);
                y_diff = abs(self.active_movement_tile.y_pos-selected_tile.y_pos);
                if (x_diff + y_diff) <= self.active_movement_tile.occupying_unit.movespeed:
                    if(selected_tile.occupied == False):
                        print("Move there!");
                        self.move_unit(selected_tile);
                    else:
                        print("Already taken");
                else:
                    print("Too far");
            else:
                if selected_tile == self.active_combat_tile:
                    print("End Movement");
                    self.deactivate_unit();
                if selected_tile in self.valid_target_tiles:
                    print("Firing!");
                    self.active_combat_tile.occupying_unit.attack_target(selected_tile.occupying_unit, True);
                    self.deactivate_unit();

    def activate_unit(self, selected_tile):
        self.active_movement_tile = selected_tile;
        #Display movement options
        tile_radius = selected_tile.occupying_unit.movespeed;
        x_center = selected_tile.x_pos;
        y_center = selected_tile.y_pos;
        y_start = max(0, y_center - tile_radius);
        y_end = min(y_dim, y_center + tile_radius);
        for j in range(y_start, y_end+1):
            horizontal_spread = tile_radius-(abs(y_center-j));
            x_start = max(0, x_center - horizontal_spread);
            x_end = min(x_dim, x_center + horizontal_spread);
            for i in range(x_start, x_end+1):
                new_overlay_tile = map_area.create_rectangle(15+box_size*i,15+box_size*j,box_size-6+box_size*i,box_size-6+box_size*j, fill="orange", activefill="blue", outline="red", width=0);
                self.overlay_tile_ids.append(new_overlay_tile);

    def display_movement_area(self):
        print("Seeking movement");
        #Store:
        #A hash(?) of checked coordinates(calculated_paths) objects. Each object has:
            #remaining movement once that tile is reached
            #most efficient path to that location
        #A Hash of lists, each hash is a different movecost
            #The lists contain an object (partial_path), which holds:
                #the paths in progress and remaining movespeed

        #Actions:
        #Get a partial_path object with the smallest movecost (any with the smallest cost is fine)
            #Generate one for the starting tile before this to get started
        #Check the calculated_paths object for the checked coordinate
            #Add it(with path/remaining movement) if it does not exist
            #If it does, compare the existing movement value to the one just calculated
            #If the new remaining movement is greater (or no data exists):
                #Overwrite the old data
                #Check each adjacent tile:
                    #If an enemy occupies it, nothing happens.
                    #Otherwise, subtract the new tile's movecost from the remaining movespeed, and add a new partial_path object to the hash
                #If it does not, the path is inefficient and the data can be discarded

        #Once done, display the possible move options
        #Iterate through the calculated_paths

    def recursive_move_check(self):
        #Don't allow backtracking - use coordinates to check? Currently just comparing to existing paths - this might be good enough
        #Prioritize checking of low-cost movement options - less overwriting

    def move_unit(self, selected_tile):
        if(selected_tile != self.active_movement_tile):
            selected_tile.assign_unit(self.active_movement_tile.occupying_unit);
            self.active_movement_tile.unassign_unit();
        self.active_combat_tile = selected_tile;
        self.activate_melee_combat_step();

    def activate_melee_combat_step(self):
        for i in self.overlay_tile_ids:
            map_area.delete(i);
        overlay_tile_ids = []; #Better way to empty a list?
        x_center = self.active_combat_tile.x_pos;
        y_center = self.active_combat_tile.y_pos;
        new_overlay_tile = map_area.create_rectangle(15+box_size*(x_center),15+box_size*(y_center),box_size-6+box_size*(x_center),box_size-6+box_size*(y_center), fill="blue", activefill="red", outline="red", width=0);
        self.overlay_tile_ids.append(new_overlay_tile);

        adjacent_coordinates = [[1,0],[-1,0],[0,1],[0,-1]];
        for i in adjacent_coordinates:
            checked_tile_id = x_center+i[0]+10*(y_center+i[1]);
            if checked_tile_id >= 0 and checked_tile_id < x_dim*y_dim:
                checked_tile = map_tile_list[checked_tile_id];
                if checked_tile.occupied == True:
                    if checked_tile.occupying_unit.team_id != self.active_combat_tile.occupying_unit.team_id:
                        print(f"Foe at{i}");
                        self.valid_target_tiles.append(checked_tile);
                        new_overlay_tile = map_area.create_rectangle(15+box_size*(x_center+i[0]),15+box_size*(y_center+i[1]),box_size-6+box_size*(x_center+i[0]),box_size-6+box_size*(y_center+i[1]), fill="orange", activefill="red", outline="red", width=0);
                        self.overlay_tile_ids.append(new_overlay_tile);


    def deactivate_unit(self):
        self.active_combat_tile.occupying_unit.complete_orders();
        for i in self.overlay_tile_ids:
            map_area.delete(i);
        self.valid_target_tiles = [];
        self.active_movement_tile = None;
        self.active_combat_tile = None;



#tkinter
main_window = tk.Tk();



def click_location(event):
    x_loc_temp = math.floor((event.x-4)/box_size);
    y_loc_temp = math.floor((event.y-4)/box_size);
    selected_tile = map_tile_list[x_loc_temp+y_loc_temp*10];
    the_game.handle_click(selected_tile);

    # map_area.itemconfig(selected_rectangle.canvas_rect_id, fill="red");

map_area = tk.Canvas(main_window, width = x_dim*box_size, height = y_dim*box_size);

map_area.bind("<Button-1>", click_location);

map_tile_list = [];



the_game = GameLogic();

for j in range(0, y_dim):
    for i in range(0,x_dim):

        new_rect_id = map_area.create_rectangle(5+box_size*i,5+box_size*j,box_size+4+box_size*i,box_size+4+box_size*j, fill="black", activefill="blue", outline="red", width=0);
        if j%2 == 0:
            move_cost_temp = 2;
        else:
            move_cost_temp = 1;
        new_rectangle = MapTile(new_rect_id, i, j, move_cost_temp);
        map_tile_list.append(new_rectangle);


map_area.pack();
test_unit = Unit(0,4,1,1);
test_unit = Unit(1,3,2,5);


main_window.mainloop();
