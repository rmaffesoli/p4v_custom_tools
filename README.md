# p4v_custom_tools
This repository is a place to park various small scripts and tools to be used in P4V as general creature comforts. The scripts are currently intentionally built to be implemented simply without any external dependencies or references to one another. Be aware that while this repetition and separation is intentional, it does cause some code duplication.

All of these scripts are designed to be added to a users P4V application as a custom tool, further technical reading can be found [here](https://www.perforce.com/manuals/p4v/Content/P4V/advanced_options.custom.html).

---

## export_p4config.py

#### Usage
Creates a basic .p4config file for the currently active workspace. If an existing .p4config exists the script will not overwrite it.

#### Arguments


---

## attach_preview.py

#### Usage

#### Arguments


---

## update_dam_preview_maya.py

#### Usage

#### Arguments

---

## update_dam_preview_max.py

#### Usage

#### Arguments

---

## update_dam_preview_blender.py

#### Usage

#### Arguments

---

## setup_for_unity

#### Usage
1. Creates a basic .p4config file for the currently active workspace. If an existing .p4config exists the script will not overwrite it.
2. Establishes a basic .p4ignore designed for unity projects. If an existing .p4ignore exists the script will not overwrite it.
3. Sets a basic Typelist for the current stream.
#### Arguments

---

## setup_for_unreal

#### Usage
1. Creates a basic .p4config file for the currently active workspace. If an existing .p4config exists the script will not overwrite it.
2. Establishes a basic .p4ignore designed for unreal projects. If an existing .p4ignore exists the script will not overwrite it.
3. Sets a basic Typelist for the current stream.
#### Arguments
