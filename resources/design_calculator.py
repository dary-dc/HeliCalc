# from .output_data import OutputData
from .utils import substraction_with_decimals
from math import sqrt, log, ceil, pi

class DesignCalculator:
    """
    Args:
    all the input data of the software

    Attributes:
    all the output data of the software

    Important points:
    1) We will handle SOME ZeroDivisionErrors in "main_window.py" by setting zero (0) as an invalid input in the DoubleSpinBoxes.
    2) coil_parameter refers to the coil-side fluid parameter. Similarly, for shell_parameter.
    """

    def __init__(self, main_window, digits_for_rounding) -> None:
        self.main_window = main_window
        self.data = main_window.input_data
        self.digits_for_rounding = digits_for_rounding
        self.rounded_pi = round(pi, digits_for_rounding)
        self.results = main_window.design_results

    def calculate_page_6(self):
        self.data.initialize_attributes_with_hot_fluid_location()
        self.results.initialize_attributes_with_hot_fluid_location()

        # calculations of the page 6
        self.results.hot_heat_load = self.heat_load(self.data.hot_Mass_flowrate, self.data.hot_Specific_heat, self.data.hot_Inlet_temperature, self.data.hot_Outlet_temperature)
        self.results.cold_heat_load = self.heat_load(self.data.cold_Mass_flowrate, self.data.cold_Specific_heat, self.data.cold_Outlet_temperature, self.data.cold_Inlet_temperature)
        self.results.average_heat_load = self.average_heat_load(self.results.hot_heat_load, self.results.cold_heat_load)

        self.results.cross_sectional_coil_area = self.cross_sectional_coil_area(self.data.Tube_inner_diameter)
        self.results.coil_volumetric_flowrate = self.volumetric_flowrate(self.data.coil_Mass_flowrate, self.data.coil_Density)
        self.results.coil_velocity = self.velocity(self.results.coil_volumetric_flowrate, self.results.cross_sectional_coil_area)
        self.results.coil_Reynolds_number = self.coil_Reynolds_number(self.data.Tube_inner_diameter, self.results.coil_velocity, self.data.coil_Density, self.data.coil_Viscosity)
        self.results.coil_Prandtl_number = self.coil_Prandtl_number(self.data.coil_Specific_heat, self.data.coil_Viscosity, self.data.coil_Thermal_conductivity)
        self.results.coil_Nusselt_number = self.coil_Nusselt_number(self.results.coil_Reynolds_number, self.results.coil_Prandtl_number)
        self.results.coil_heat_transfer_coeficient = self.coil_heat_transfer_coeficient(self.results.coil_Nusselt_number, self.data.coil_Thermal_conductivity, self.data.Tube_inner_diameter)
        self.results.coil_heat_transfer_coeficient_inside_diameter = self.coil_heat_transfer_coeficient_inside_diameter(self.results.coil_heat_transfer_coeficient, self.data.Tube_inner_diameter, self.data.Average_spiral_diameter)
        self.results.coil_heat_transfer_coeficient_outside_diameter = self.coil_heat_transfer_coeficient_outside_diameter(self.results.coil_heat_transfer_coeficient_inside_diameter, self.data.Tube_inner_diameter, self.data.Tube_outer_diameter)

        self.results.outer_spiral_diameter = self.outer_spiral_diameter(self.data.Shell_inner_diameter, self.data.Tube_outer_diameter)
        self.results.inner_spiral_diameter = self.inner_spiral_diameter(self.data.Core_tube_outer_diameter, self.data.Tube_outer_diameter)
        self.results.shell_flow_cross_section = self.shell_flow_cross_section(self.data.Shell_inner_diameter, self.data.Core_tube_outer_diameter, self.results.outer_spiral_diameter, self.results.inner_spiral_diameter)
        self.results.shell_volumetric_flowrate = self.volumetric_flowrate(self.data.shell_Mass_flowrate, self.data.shell_Density)
        self.results.shell_velocity = self.velocity(self.results.shell_volumetric_flowrate, self.results.shell_flow_cross_section)
        self.results.length_coil_needed = self.length_coil_needed(self.data.Average_spiral_diameter, self.data.Tube_pitch)
        self.results.volume_occupied_by_coil = self.volume_occupied_by_coil(self.data.Tube_outer_diameter, self.results.length_coil_needed)
        self.results.volume_of_shell = self.volume_of_shell(self.data.Shell_inner_diameter, self.data.Core_tube_outer_diameter, self.data.Tube_pitch)
        self.results.volume_available_flow_shell = self.volume_available_flow_shell(self.results.volume_of_shell, self.results.volume_occupied_by_coil)
        self.results.equivalent_diameter = self.equivalent_diameter(self.results.volume_available_flow_shell, self.data.Tube_outer_diameter, self.results.length_coil_needed)
        self.results.shell_Reynolds_number = self.shell_Reynolds_number(self.results.equivalent_diameter, self.results.shell_velocity, self.data.shell_Density, self.data.shell_Viscosity)
        self.results.shell_Prandtl_number = self.shell_Prandtl_number(self.data.shell_Specific_heat, self.data.shell_Viscosity, self.data.shell_Thermal_conductivity)
        self.results.shell_heat_transfer_coeficient = self.shell_heat_transfer_coeficient(self.data.shell_Thermal_conductivity, self.results.equivalent_diameter, self.results.shell_Reynolds_number, self.results.shell_Prandtl_number)

    def calculate_page_7(self):
        # calculations of the page 7
        self.results.coil_wall_thickness = self.coil_wall_thickness(self.data.Tube_outer_diameter, self.data.Tube_inner_diameter)
        self.results.overall_heat_transfer_coeficient = self.overall_heat_transfer_coeficient(self.results.coil_heat_transfer_coeficient_outside_diameter, self.results.shell_heat_transfer_coeficient, self.results.coil_wall_thickness, self.data.Thermal_conductivity_coil_material, self.data.shell_Fouling_factor, self.data.coil_Fouling_factor)
        self.results.log_mean_temp_difference = self.log_mean_temp_difference(self.data.hot_Inlet_temperature, self.data.cold_Outlet_temperature, self.data.hot_Outlet_temperature, self.data.cold_Inlet_temperature)
        self.results.effective_mean_temperature_difference = self.effective_mean_temperature_difference(self.results.log_mean_temp_difference, self.data.Temperature_correction_factor)
        self.results.spiral_total_surface_area = self.spiral_total_surface_area(self.results.average_heat_load, self.results.overall_heat_transfer_coeficient, self.results.effective_mean_temperature_difference)
        self.results.number_of_turns_coil = self.number_of_turns_coil(self.results.spiral_total_surface_area, self.data.Tube_outer_diameter, self.results.length_coil_needed)
        self.results.calculated_spiral_total_tube_length = self.calculated_spiral_total_tube_length(self.results.length_coil_needed, self.results.number_of_turns_coil)
        self.results.height_of_cylinder = self.height_of_cylinder(self.results.number_of_turns_coil, self.data.Tube_pitch, self.data.Tube_outer_diameter)

    def calculate_page_8(self):
        # calculations of the page 8
        self.results.coil_Factor_E = self.coil_Factor_E(self.data.Average_spiral_diameter, self.data.Tube_pitch)
        self.results.coil_Friction_factor = self.coil_Friction_factor(self.results.coil_Reynolds_number, self.data.Tube_inner_diameter, self.results.coil_Factor_E)
        self.results.coil_Pressure_drop = self.coil_Pressure_drop(self.results.coil_Friction_factor, self.results.calculated_spiral_total_tube_length, self.data.Tube_inner_diameter, self.results.coil_velocity, self.data.coil_Density)
        self.results.shell_drag_coeficient = self.shell_drag_coeficient(self.results.shell_Reynolds_number, self.data.Tube_outer_diameter, self.data.Average_spiral_diameter)
        self.results.shell_Pressure_drop = self.shell_Pressure_drop(self.results.shell_drag_coeficient, self.results.height_of_cylinder, self.results.equivalent_diameter, self.results.shell_velocity, self.data.shell_Density)
        self.results.coil_Pumping_power = self.coil_Pumping_power(self.results.coil_Pressure_drop, self.data.coil_Mass_flowrate, self.data.coil_Isentropic_efficiency_pump, self.data.coil_Density)
        self.results.shell_Pumping_power = self.shell_Pumping_power(self.results.shell_Pressure_drop, self.data.shell_Mass_flowrate, self.data.shell_Isentropic_efficiency_pump, self.data.shell_Density)


    # all the calculations for the desgin 
    # calculations of the page 6 in the software
    # step 4 in methodology
    def heat_load(self, mass_flowrate, specific_heat, inlet_temperature, outlet_temperature):
        return round((mass_flowrate * specific_heat * (inlet_temperature - outlet_temperature)) / 3600, 7)

    # def cold_fluid_heat_load(self, cold_mass_flowrate, cold_specific_heat, cold_outlet_temperature, cold_inlet_temperature):
    #     return round((cold_mass_flowrate * cold_specific_heat * (cold_outlet_temperature - cold_inlet_temperature)) / 3600, 7)

    # implemented in the ErrorHandler class because of the possible error that could be raised
    def hot_heat_load_cold_heat_load_ratio(self):
        pass

    # step 5 in methodology
    def average_heat_load(self, hot_heat_load, cold_heat_load):
        return (hot_heat_load + cold_heat_load) / 2
        # return round((hot_heat_load + cold_heat_load) / 2, self.digits_for_rounding)

    # step 7 in methodology
    def cross_sectional_coil_area(self, tube_inner_diameter):
        return round((self.rounded_pi * tube_inner_diameter ** 2) / 4, self.digits_for_rounding)
        
    # for coil and shell fluids
    # step 8 in methodology
    # step 19 in methodology
    def volumetric_flowrate(self, mass_flowrate, density):
        return round(mass_flowrate / density / 3600, self.digits_for_rounding)

    # for coil and shell fluids
    # step 9 in methodology
    # step 20 in methodology
    def velocity(self, volumetric_flowrate, cross_sectional_area):
        """
        Args:
        for fluid in shell:
        Volumetric flowrate of the shell-side fluid
        Shell-side flow cross-section 

        for fluid in coil:
        Volumetric flowrate of coil-side fluid
        Cross-sectional area of coil
        """
        try:
            return round(volumetric_flowrate / cross_sectional_area, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'velocity'")
            print(e)
            # self.main_window.error_handler.warn_incorrect_input()

    # step 10 in methodology
    def coil_Reynolds_number(self, Tube_inner_diameter, coil_velocity, coil_Density, coil_Viscosity):
        try:
            return round((Tube_inner_diameter * coil_velocity * coil_Density) / coil_Viscosity, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Reynolds_number'")
            print(e)

    # step 11 in methodology
    def coil_Prandtl_number(self, coil_Specific_heat, coil_Viscosity, coil_Thermal_conductivity):
        try:
            return round(((coil_Specific_heat * coil_Viscosity) / coil_Thermal_conductivity) * 1000, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Prandtl_number'")
            print(e)

    # step 12 in methodology
    def coil_Nusselt_number(self, coil_Reynolds_number, coil_Prandtl_number):
        try:
            print("coil_Reynolds_number:", coil_Reynolds_number)
            if coil_Reynolds_number <= 2300: # this sofware doesn't support fluids with Reynolds number values smaller than 2300
                return -1
            
            # if 2300 < coil_Reynolds_number < 8000
            if coil_Reynolds_number < 8000: # added in version 3.0 (for transition regime)
                coil_Nusselt_number = round((0.037 * (coil_Reynolds_number ** 0.75) - 6.66) * (coil_Prandtl_number ** 0.42), self.digits_for_rounding)
            else: # elif coil_Reynolds_number >= 8000:
                coil_Nusselt_number = round(0.023 * (coil_Reynolds_number ** 0.8) * (coil_Prandtl_number ** 0.33), self.digits_for_rounding)
            return coil_Nusselt_number
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Nusselt_number'")
            print(e)


    # step 13 in methodology
    def coil_heat_transfer_coeficient(self, coil_Nusselt_number, coil_Thermal_conductivity, Tube_inner_diameter):
        try:
            return round(coil_Nusselt_number * coil_Thermal_conductivity / Tube_inner_diameter, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_heat_transfer_coeficient'")
            print(e)
        
    # step 14 in methodology
    def coil_heat_transfer_coeficient_inside_diameter(self, coil_heat_transfer_coeficient, tube_inner_diameter, average_spiral_diameter):
        try:
            return round(coil_heat_transfer_coeficient * (1 + 3.5 * tube_inner_diameter / average_spiral_diameter), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_heat_transfer_coeficient_inside_diameter'")
            print(e)
        
    # step 15 in methodology
    def coil_heat_transfer_coeficient_outside_diameter(self, coil_heat_transfer_coeficient_inside_diameter, tube_inner_diameter, tube_outer_diameter):
        try:
            return round(coil_heat_transfer_coeficient_inside_diameter * tube_inner_diameter / tube_outer_diameter, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_heat_transfer_coeficient_outside_diameter'")
            print(e)
        
    # step 16 in methodology
    def outer_spiral_diameter(self, Shell_inner_diameter, Tube_outer_diameter):
        try:
            return round(substraction_with_decimals(Shell_inner_diameter, Tube_outer_diameter), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'outer_spiral_diameter'")
            print(e)
        
    # step 17 in methodology
    def inner_spiral_diameter(self, Core_tube_outer_diameter, Tube_outer_diameter):
        try:
            return round(Core_tube_outer_diameter + Tube_outer_diameter, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'inner_spiral_diameter'")
            print(e)
        
    # step 18 in methodology
    def shell_flow_cross_section(self, Shell_inner_diameter, Core_tube_outer_diameter, outer_spiral_diameter, inner_spiral_diameter):
        try:
            return round(self.rounded_pi/4 * ((Shell_inner_diameter**2 - Core_tube_outer_diameter**2) - (outer_spiral_diameter**2 - inner_spiral_diameter**2)), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'shell_flow_cross_section'")
            print(e)
        
    # (there are two equal formulas)

    # step 21 in methodology
    def length_coil_needed(self, average_spiral_diameter, tube_pitch):
        # return round(sqrt((self.rounded_pi * average_spiral_diameter)**2 - tube_pitch**2), self.digits_for_rounding)
        try:
            return round(sqrt((self.rounded_pi * average_spiral_diameter)**2 + tube_pitch**2), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'length_coil_needed'")
            print(e)
    
    # step 22 in methodology
    def volume_occupied_by_coil(self, tube_outer_diameter, length_coil_needed):
        try:
            return round(self.rounded_pi/4 * (tube_outer_diameter**2) * length_coil_needed, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'volume_occupied_by_coil'")
            print(e)
        
    # step 23 in methodology
    def volume_of_shell(self, shell_inner_diameter, core_tube_outer_diameter, tube_pitch):
        try:
            return round(self.rounded_pi/4 * (shell_inner_diameter**2 - core_tube_outer_diameter**2) * tube_pitch, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'volume_of_shell'")
            print(e)
        
    # step 24 in methodology
    def volume_available_flow_shell(self, volume_of_shell, volume_occupied_by_coil):
        try:
            return round(volume_of_shell - volume_occupied_by_coil, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'volume_available_flow_shell'")
            print(e)
        
    # step 25 in methodology
    def equivalent_diameter(self, volume_available_flow_shell, tube_outer_diameter, length_coil_needed):
        try:
            return round((4 * volume_available_flow_shell) / (self.rounded_pi * tube_outer_diameter * length_coil_needed), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'equivalent_diameter'")
            print(e)
        
    # step 26 in methodology
    def shell_Reynolds_number(self, equivalent_diameter, shell_velocity, shell_density, shell_viscosity):
        try:
            return round((equivalent_diameter * shell_velocity * shell_density) / shell_viscosity, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'shell_Reynolds_number'")
            print(e)
        
    # step 27 in methodology
    def shell_Prandtl_number(self, shell_specific_heat, shell_viscosity, shell_thermal_conductivity):
        try:
            return round(((shell_specific_heat * shell_viscosity) / shell_thermal_conductivity) * 1000, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'shell_Prandtl_number'")
            print(e)
        
    # step 28 in methodology
    def shell_heat_transfer_coeficient(self, shell_thermal_conductivity, equivalent_diameter, shell_Reynolds_number, shell_Prandtl_number):
        print("Error is in heat transfer coeficient")
        print("shell_Reynolds_number:", shell_Reynolds_number)

        try:
            if shell_Reynolds_number <= 50:
                return -1
            
            # if 50 < shell_Reynolds_number < 10 000
            if shell_Reynolds_number < 10000:
                shell_heat_transfer_coeficient = round(0.6 * (shell_thermal_conductivity / equivalent_diameter) * (shell_Reynolds_number**0.5) * (shell_Prandtl_number**0.31), self.digits_for_rounding)
            else: # elif shell_Prandtl_number >= 10 000
                shell_heat_transfer_coeficient = round(0.36 * (shell_thermal_conductivity / equivalent_diameter) * (shell_Reynolds_number**0.55) * (shell_Prandtl_number**0.33), self.digits_for_rounding)
            return shell_heat_transfer_coeficient
        except Exception as e:
            print("Error in method of disign calculator: 'shell_heat_transfer_coeficient'")
            print(e)



    # calculations of the page 7 in the software
    # step 29 in methodology
    def coil_wall_thickness(self, Tube_outer_diameter, Tube_inner_diameter):
        try:
            return round((substraction_with_decimals(Tube_outer_diameter, Tube_inner_diameter)) / 2, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_wall_thickness'")
            print(e)
        
    # step 30 in methodology
    def overall_heat_transfer_coeficient(self, coil_heat_transfer_coeficient_outside_diameter, shell_heat_transfer_coeficient, coil_wall_thickness, Thermal_conductivity_coil_material, shell_Fouling_factor, coil_Fouling_factor):
        try:
            return round(1 / ((1 / coil_heat_transfer_coeficient_outside_diameter) + (1 / shell_heat_transfer_coeficient) + (coil_wall_thickness / Thermal_conductivity_coil_material) + shell_Fouling_factor + coil_Fouling_factor), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'overall_heat_transfer_coeficient'")
            print(e)

    # step 31 in methodology
    def log_mean_temp_difference(self, hot_Inlet_temperature, cold_Outlet_temperature, hot_Outlet_temperature, cold_Inlet_temperature):
        try:
            return round(((hot_Inlet_temperature - cold_Outlet_temperature) - (hot_Outlet_temperature - cold_Inlet_temperature)) / (log((hot_Inlet_temperature - cold_Outlet_temperature) / (hot_Outlet_temperature - cold_Inlet_temperature))), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'log_mean_temp_difference'")
            print(e)
            return e
        
    # step 32 in methodology
    def effective_mean_temperature_difference(self, log_mean_temp_difference, Temperature_correction_factor):
        try:
            return round(log_mean_temp_difference * Temperature_correction_factor, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'effective_mean_temperature_difference'")
            print(e)
        
    # step 33 in methodology
    def spiral_total_surface_area(self, Qe, overall_heat_transfer_coeficient, effective_mean_temperature_difference):
        try:
            return round((Qe / (overall_heat_transfer_coeficient * effective_mean_temperature_difference)) * 1000, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'spiral_total_surface_area'")
            print(e)
        
    # step 34 in methodology
    def number_of_turns_coil(self, spiral_total_surface_area, Tube_outer_diameter, length_coil_needed):
        try:
            return ceil(spiral_total_surface_area / (self.rounded_pi * Tube_outer_diameter * length_coil_needed))
        except Exception as e:
            print("Error in method of disign calculator: 'number_of_turns_coil'")
            print(e)
        
    # step 35 in methodology
    def calculated_spiral_total_tube_length(self, length_coil_needed, number_of_turns_coil):
        try:
            return round(length_coil_needed * number_of_turns_coil, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'calculated_spiral_total_tube_length'")
            print(e)
        
    # step 36 in methodology
    def height_of_cylinder(self, number_of_turns_coil, Tube_pitch, Tube_outer_diameter):
        try:
            return round(number_of_turns_coil * Tube_pitch + Tube_outer_diameter, self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'height_of_cylinder'")
            print(e)


    # calculations of the page 8 in the software
    # step 37 in methodology
    def coil_Factor_E(self, Average_spiral_diameter, Tube_pitch):
        try:
            return round(Average_spiral_diameter * (1 + (Tube_pitch / (self.rounded_pi * Average_spiral_diameter)) ** 2), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Factor_E'")
            print(e)
        
    # step 38 in methodology
    def coil_Friction_factor(self, coil_Reynolds_number, Tube_inner_diameter, coil_Factor_E):
        try:
            return round(((0.3164 / (coil_Reynolds_number**0.25) + 0.03*((Tube_inner_diameter / coil_Factor_E)**(1/2)) )) * 1, self.digits_for_rounding) # (miu_w / miu)**0.27 = 1 as suggested by (Andrzejczyk & Muszynski, 2016). See methodology
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Friction_factor'")
            print(e)
        
    # step 40 in methodology
    def coil_Pressure_drop(self, coil_Friction_factor, calculated_spiral_total_tube_length, Tube_inner_diameter, coil_velocity, coil_Density):
        try:
            return round(coil_Friction_factor * (calculated_spiral_total_tube_length/Tube_inner_diameter) * ((coil_velocity**2 * coil_Density)/2), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Pressure_drop'")
            print(e)
        
    # step 39 in methodology
    def shell_drag_coeficient(self, shell_Reynolds_number, Tube_outer_diameter, Average_spiral_diameter):
        try:
            return round((0.3164 / (shell_Reynolds_number**0.25)) * (1 + (0.095 * ((Tube_outer_diameter/Average_spiral_diameter)**0.5)) * (shell_Reynolds_number**0.25)), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'shell_drag_coeficient'")
            print(e)

    # step 41 in methodology
    def shell_Pressure_drop(self, shell_drag_coeficient, height_of_cylinder, equivalent_diameter, shell_velocity, shell_Density):
        try:
            return round(shell_drag_coeficient * (height_of_cylinder / equivalent_diameter) * ((shell_velocity**2 * shell_Density)/2), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'shell_Pressure_drop'")
            print(e)
        
    # step 42 in methodology
    def coil_Pumping_power(self, coil_Pressure_drop, coil_Mass_flowrate, coil_Isentropic_efficiency_pump, coil_Density):
        try:
            return round((coil_Pressure_drop * (coil_Mass_flowrate / 3600)) / (coil_Isentropic_efficiency_pump * coil_Density), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'coil_Pumping_power'")
            print(e)
        
    # step 43 in methodology
    def shell_Pumping_power(self, shell_Pressure_drop, shell_Mass_flowrate, shell_Isentropic_efficiency_pump, shell_Density):
        try:
            return round((shell_Pressure_drop * (shell_Mass_flowrate / 3600)) / (shell_Isentropic_efficiency_pump * shell_Density), self.digits_for_rounding)
        except Exception as e:
            print("Error in method of disign calculator: 'shell_Pumping_power'")
            print(e)


    # page 8. Added in version 3.0
    def get_comprarison_pressure_values(self):
        try:
            return {"coil": self.data.coil_Allowable_pressure_drop >= self.results.coil_Pressure_drop,
                    "shell": self.data.shell_Allowable_pressure_drop >= self.results.shell_Pressure_drop}
        except Exception as e:
            print("Error in method of disign calculator: 'get_comprarison_pressure_values'")
            print(e)
