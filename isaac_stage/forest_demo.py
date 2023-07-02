from omni.isaac.kit import SimulationApp
simulation_app = SimulationApp({"headless": True})

from pathlib import Path
import omni    

from omni.isaac.core.simulation_context import SimulationContext

from assets import *
from isaac_stage.assets import AssetManager
import isaac_stage.prims
from isaac_stage.terrain import *
from isaac_stage.stage_builder import ConstructionStageBuilder, ForestStageBuilder
from isaac_stage.appliers import apply_appliers, apply_color_to_prim, apply_default_ground_physics_material

from omni.isaac.orbit.markers import PointMarker



"""
Source: https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/reference_python_snippets.html

According to the source above a valid raycast call requires the following: 
 1. the stage contains a physics scene, 
 2. all objects have collision meshes enabled 
 3. the play button has been clicked
"""

class IsaacSimRunner(object):
    """Runs omniverse."""
    def __init__(self):
        physics_dt = 1 / 100.0
        render_dt = 1 / 30.0
        self._world = SimulationContext(stage_units_in_meters=1.0, physics_dt=physics_dt, rendering_dt=render_dt, backend="torch")

    def on_physics_step(self,stepsize:float):
        pass 

    def run(self) -> None:
        """Step simulation based on rendering downtime"""

        self._world.reset()
        
        # change to sim running
        while simulation_app.is_running():
            #self.rayTraceRandomPoints()
            self._world.step(render=True)
        return

#-----------------------------------------------------------#
#   basic program demonstrating how the scene is produced   #
#-----------------------------------------------------------#

def main():    
    # open/load pre-built stage
    # get_context().open_stage(str(Path("PATH_TO_STAGE.usd*"),relative_pathing=True)
    # NOTE: This needs to happen before IsaacSimRunner()'s init
    # NOTE 2: Name collisions are a problem in general in this file.
    # This scene was saved with the same raytracing test that is initialized 
    # during the testing so those prims have name collisions.


    """Runs the simulation via the IsaacSimRunner."""
    isaac_sim_runner = IsaacSimRunner()
    simulation_app.update()

    # safe to set up here
    #------------#
    #   assets   #
    #------------#

    # create asset manager
    asset_manager = AssetManager()

    # register assets with a default material that 1) enables collisions 2) makes them visible to physics raytracing. NOTE: The ground material is static, i.e., objects cannot move.
    asset_manager.register_asset("./assets/Forest/pine.usd", asset_scale=0.02, applier=apply_default_ground_physics_material)
    asset_manager.register_asset("./assets/Forest/bush.usd", asset_scale=0.01, applier=apply_default_ground_physics_material)
    asset_manager.register_asset("./assets/Forest/thyme_bush.usd", asset_scale=1.3, applier=apply_default_ground_physics_material)
    asset_manager.register_asset("./assets/Forest/square_rock.usd", asset_scale=0.175, applier=apply_default_ground_physics_material)
    asset_manager.register_asset("./assets/Forest/large_dirt_pile.usd", asset_scale=0.075, applier=apply_default_ground_physics_material)
    asset_manager.register_asset("./assets/Forest/oak_tree_variation.usd", asset_scale=0.02, applier=apply_default_ground_physics_material)
    asset_manager.register_asset("./assets/Forest/moss_rock_photoscan.usd", asset_scale=0.015, applier=apply_default_ground_physics_material)


    #-------------#
    #   terrain   #
    #-------------#

    dim = 100 # both terrain and environment

    # define terrain function
    terrain = ForestedRoadsTerrain(terrain_unit=0.5, xdim=dim, ydim=dim, amp=0.15, spawn_radius=5.5,road_min_width=0.15, road_max_width=1.5, road_num=13, border_threshold=10
                                   ,applier=apply_appliers([apply_default_ground_physics_material, lambda prim_path : apply_color_to_prim(prim_path, color=(49/255,36/255,25/255))]))

    #-----------------#
    #   environment   #
    #-----------------#

    # create environment object
    environment = ForestStageBuilder(xdim=dim,ydim=dim,terrain=terrain,asset_manager=asset_manager)
    
    # build stage
    environment.build_stage(global_offset=[0,0,0],spawn_assets=True,asset_density=5)  

    # save stage
    environment.save_stage("../stages/forest_demo_bordered_bowl.usdc")

    # everything after this line happens at until the simulation is closed
    isaac_sim_runner.run() # Process continues until closed by user or exception.

    # post simulation events go here

    simulation_app.close()

if __name__ == "__main__":
    main()
