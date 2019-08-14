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
        selected_tile = x_in+x_dim*y_in;
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
        self.display_movement_area(tile_radius);
        """
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
        """

    def create_path(self, path_string_in, remaining_movement_in, x_distance, y_distance):
        new_path_dictionary = {
            "remaining_movespeed" : remaining_movement_in,
            "path" : path_string_in,
            "x_diff" : x_distance,
            "y_diff" : y_distance,
        };
        print("New path dictionary complete");
        return new_path_dictionary;

    def display_movement_area(self, initial_movespeed):
        x_center = self.active_movement_tile.x_pos;
        y_center = self.active_movement_tile.y_pos;
        path_zone_length = 2*initial_movespeed+1;
        print("Seeking movement");
        #Store:
        #A list(2-D?) of checked coordinates(calculated_paths) dictionaries. Each dictionary has:
            #remaining movement once that tile is reached
            #most efficient path to that location
        calculated_paths = ["NA"]*(path_zone_length**2);
        calculated_paths_remaining_movement = [-1]*(path_zone_length**2);

        #A Dictionary of lists, each key is a different movecost
            #The lists contain a dictionary (partial_path), which holds:
                #the paths in progress and remaining movespeed
        initial_square = self.create_path("",initial_movespeed, 0, 0);
        partial_paths = {
            "cost_1" : [initial_square],
        };

        print(partial_paths);
        #Actions:
        #Get a partial_path dictionary with the smallest movecost (any with the smallest cost is fine)
            #Generate one for the starting tile before this to get started
        while(len(partial_paths["cost_1"]) > 0):
            path_to_check = partial_paths["cost_1"].pop(0);
            #Check the calculated_paths object for the checked coordinate
            x_map_coordinate = x_center+path_to_check["x_diff"];
            y_map_coordinate = y_center+path_to_check["y_diff"];

            map_tile_to_check = map_tile_list[x_map_coordinate + y_map_coordinate*x_dim];
            calculated_path_index = (initial_movespeed + path_to_check["x_diff"]) + path_zone_length * (initial_movespeed + path_to_check["y_diff"]);
            #print("x_diff:", path_to_check["x_diff"]);
            #print("y_diff:", path_to_check["y_diff"]);
            #print("path zone length:", path_zone_length);
            print("Calc'ed path index:", calculated_path_index);
            if calculated_paths_remaining_movement[calculated_path_index] < path_to_check["remaining_movespeed"]:
                print("Better path - overwrite data!");
                calculated_paths[calculated_path_index] = path_to_check["path"];
                calculated_paths_remaining_movement[calculated_path_index] = path_to_check["remaining_movespeed"];
                #Make new paths here - check the new tiles for validity here

                #up, right, down, left
                coordinate_offsets = [[0,-1],[1,0],[0,1],[-1,0]];
                direction_string = ["U", "R", "D", "L"];
                for i in range(0, 4):
                    new_map_x_coord = x_map_coordinate + coordinate_offsets[i][0];
                    new_map_y_coord = y_map_coordinate + coordinate_offsets[i][1];
                    map_tile_index = new_map_x_coord + new_map_y_coord * x_dim;
                    print(map_tile_index, "MTI")
                    print(new_map_x_coord, "x_cor")
                    print(new_map_y_coord, "y_cor")
                    #Boundary check
                    if new_map_x_coord >= 0 and new_map_x_coord < x_dim and new_map_y_coord >= 0 and new_map_y_coord < y_dim and map_tile_index >=0 and map_tile_index < x_dim*y_dim:
                        map_tile_to_check = map_tile_list[map_tile_index];
                        #Enemy presence check:
                        enemy_presence = False;
                        if map_tile_to_check.occupied:
                            if map_tile_to_check.occupying_unit.team_id != self.active_movement_tile.occupying_unit.team_id:
                                enemy_presence = True;

                        if (not enemy_presence):
                            #(map_tile_index >= 0 and map_tile_index < x_dim*y_dim):

                            new_remaining_movement = path_to_check["remaining_movespeed"] - map_tile_to_check.move_cost;
                            if(new_remaining_movement >= 0):
                                new_path = self.create_path(path_to_check["path"]+direction_string[i], new_remaining_movement, path_to_check["x_diff"]+coordinate_offsets[i][0], path_to_check["y_diff"]+coordinate_offsets[i][1]);
                                partial_paths["cost_1"].append(new_path);

                #Add it(with path/remaining movement) if it does not exist
                #If it does, compare the existing movement value to the one just calculated
                #If the new remaining movement is greater (or no data exists):
                    #Overwrite the old data
                    #Check each adjacent tile if remaining movement > 0:
                        #If an enemy occupies it, nothing happens.
                        #If the unit cannot move there due to terrain (not enough movement, or non-traversible tile), nothing happens
                        #Otherwise, subtract the new tile's movecost from the remaining movespeed, and add a new partial_path object to the hash
                    #If it does not, the path is inefficient and the data can be discarded


            for j in range(0, path_zone_length):
                print(calculated_paths_remaining_movement[j*path_zone_length:((j+1)*path_zone_length)]);
                #print(calculated_paths[j*path_zone_length:((j+1)*path_zone_length)]);
            #print(partial_paths["cost_1"]);
        #Once done, display the possible move options
        #Iterate through the calculated_paths list, display an overlay for each relevant tile

        #minimum
        #Case 1: movement region within map, does not touch upper border
            #Minimum: 0
            #Maximum: 0+path_zone_length(not inclusive)
        #Case 2: movement region extends beyond borders
            #Minimum: initial_movespeed - y_center
            #maximum:
                #movement>mapsize:
        print("NEW MAP");
        y_start = max(0, initial_movespeed - y_center);
        y_end = path_zone_length;
        y_end = min(y_end, y_start+y_dim);

        x_start = max(0, initial_movespeed - x_center);
        x_end = path_zone_length;
        x_end = min(x_end, x_start + x_dim);

        print(y_start, y_end)
        print(x_start, x_end)
        y_offset = initial_movespeed - y_center;
        x_offset = initial_movespeed - x_center;
        for j in range(y_start, y_end):
            print(calculated_paths_remaining_movement[j*path_zone_length + x_start:(j*path_zone_length+x_end)]);
            for i in range(x_start,x_end):
                print(i,j);
                if(calculated_paths_remaining_movement[j*path_zone_length + i] >= 0):
                    new_overlay_tile = map_area.create_rectangle(15+box_size*(i-x_offset),15+box_size*(j-y_offset),box_size-6+box_size*(i-x_offset),box_size-6+box_size*(j-y_offset), fill="orange", activefill="blue", outline="red", width=0);
                    self.overlay_tile_ids.append(new_overlay_tile);
        #x_center = selected_tile.x_pos;
        #y_center = selected_tile.y_pos;
        """
        y_start = max(0, y_center - tile_radius);
        y_end = min(y_dim, y_center + tile_radius);
        for j in range(y_start, y_end+1):
            horizontal_spread = tile_radius-(abs(y_center-j));
            x_start = max(0, x_center - horizontal_spread);
            x_end = min(x_dim, x_center + horizontal_spread);
            for i in range(x_start, x_end+1):
                new_overlay_tile = map_area.create_rectangle(15+box_size*i,15+box_size*j,box_size-6+box_size*i,box_size-6+box_size*j, fill="orange", activefill="blue", outline="red", width=0);
                self.overlay_tile_ids.append(new_overlay_tile);
                """

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
test_unit = Unit(0,8,2,3);

test_unit = Unit(1,3,2,5);
test_unit = Unit(1,3,4,5);
test_unit = Unit(1,3,3,4);
test_unit = Unit(1,3,3,6);

test_unit = Unit(1,3,0,7);
test_unit = Unit(1,3,1,8);
test_unit = Unit(1,3,2,9);


main_window.mainloop();
