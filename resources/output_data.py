
class OutputData:
    def __init__(self):
        self.hot_in_shell = False
        self.hot_in_coil = False

        # results of the page 6
        self.hot_heat_load = 0
        self.cold_heat_load = 0
        self.Qh_Qc_ratio = 0
        self.average_heat_load = 0

        # this two will get updated according to the location of the hot fluid
        # through the method initialize_attributes_with_hot_fluid_location()
        self.shell_heat_laod = 0 # Qh
        self.coil_heat_load = 0 # Qc

        self.cross_sectional_coil_area = 0
        self.coil_volumetric_flowrate = 0
        self.coil_velocity = 0
        self.coil_Reynolds_number = 0
        self.coil_Prandtl_number = 0
        self.coil_Nusselt_number = 0
        self.coil_heat_transfer_coeficient = 0
        self.coil_heat_transfer_coeficient_inside_diameter = 0
        self.coil_heat_transfer_coeficient_outside_diameter = 0

        self.outer_spiral_diameter = 0
        self.inner_spiral_diameter = 0
        self.shell_flow_cross_section = 0
        self.shell_volumetric_flowrate = 0
        self.shell_velocity = 0
        self.length_coil_needed = 0
        self.volume_occupied_by_coil = 0
        self.volume_of_shell = 0
        self.volume_available_flow_shell = 0
        self.equivalent_diameter = 0
        self.shell_Reynolds_number = 0
        self.shell_Prandtl_number = 0
        self.shell_heat_transfer_coeficient = 0

        # results of the page 7
        self.coil_wall_thickness = 0
        self.overall_heat_transfer_coeficient = 0
        self.log_mean_temp_difference = 0
        self.effective_mean_temperature_difference = 0
        self.spiral_total_surface_area = 0
        self.number_of_turns_coil = 0
        self.calculated_spiral_total_tube_length = 0
        self.height_of_cylinder = 0

        # results of the page 8
        self.coil_Factor_E = 0
        self.coil_Friction_factor = 0
        self.coil_Pressure_drop = 0
        self.shell_drag_coeficient = 0
        self.shell_Pressure_drop = 0
        self.coil_Pumping_power = 0
        self.shell_Pumping_power = 0
        
    def initialize_attributes_with_hot_fluid_location(self):
        if self.hot_in_shell:
            self.shell_heat_laod = self.hot_heat_load # Qh
            self.coil_heat_load = self.cold_heat_load # Qc

        elif self.hot_in_coil:
            self.coil_heat_load = self.hot_heat_load # Qh
            self.shell_heat_laod = self.cold_heat_load # Qc
