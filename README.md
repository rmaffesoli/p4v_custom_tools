# p4v_custom_tools
This repository is a place to park various small scripts and tools to be used in P4V as general creature comforts. The scripts are currently intentionally built to be implemented simply without any external dependencies or references to one another. Be aware that while this repetition and separation is intentional, it does cause some code duplication. This is also the initial reasoning behind placing the file templates for the p4config, p4ignore, and p4typemap files directly in the python scripts as opposed to reading these templates from a single file location or performing any package imports.

All of these scripts are designed to be added to a users P4V application as a custom tool, further technical reading can be found [here](https://www.perforce.com/manuals/p4v/Content/P4V/advanced_options.custom.html).

---

## import_rm_tools.xml

#### Usage
This xml file can be used to import the P4V specific custom tools into your own P4V instance.
You will need to edit the script paths prior to import to replace the `YOUR_PATH` portion to reflect the script location on your specific machine.

---

## export_p4config.py

#### Usage
Creates a basic .p4config file for the currently active workspace. If an existing `.p4config` file exists the script will not overwrite it.

#### Arguments

`YOUR_PATH/p4v_custom_tools/export_p4config.py $r $p $c $u`

---

## setup_for_unreal.py

#### Usage

1. Creates a basic .p4config file for the currently active workspace. If an existing `.p4config` exists the script will not overwrite it.
2. Establishes a basic .p4ignore designed for unreal projects. If an existing `.p4ignore` exists the script will not overwrite it.
3. Sets a basic unreal style P4 type list for the current stream.
4. the user will be prompted to provide the name of the UE project.

#### Arguments

`YOUR_PATH/p4v_custom_tools/setup_for_unreal.py $r $p $c $u`
1. script_path
2. workspace root
3. P4PORT
4. Workspace Name
5. username
6. Unreal engine project name (prompt)

---

## setup_for_unity.py

#### Usage

1. Creates a basic .p4config file for the currently active workspace. If an existing `.p4config` exists the script will not overwrite it.
2. Establishes a basic .p4ignore designed for unity projects. If an existing `.p4ignore` exists the script will not overwrite it.
3. Sets a basic unity style P4 type list for the current stream.

#### Arguments

`YOUR_PATH/p4v_custom_tools/p4v_custom_tools/setup_for_unity.py $r $p $c $u`
1. script_path
2. workspace root
3. P4PORT
4. Workspace Name
5. username

---

## attach_preview.py

#### Usage

This script can be used from P4V to attach a give image to a selected workspace file as a preview. The user runs the tool with a current selection (single file) and will be prompted to provide the image path via dialog.

#### Arguments

`YOUR_PATH/p4v_custom_tools/p4v_custom_tools/attach_preview.py %f <image_filepath>`
1. Selected filepath from P4V interface
2. image_filepath to use (prompt)

---

## update_dam_preview_maya.py

#### Usage

Intended to be added as a custom Shelf button into Maya. When clicked while you have a Maya scene open within a P4 client workspace it will take a screenshot of your current viewport and attach it to your the current revision in Helix Core as a hex encoded value. This Value will then be visible in Helix DAM as a preview image.

#### Arguments

None. The current open scene name will be used.

---

## update_dam_preview_max.py


#### Usage
Intended to be run as a custom script in 3DSMax. When clicked while you have a 3DSMax scene open within a P4 client workspace it will take a screenshot of your current viewport and attach it to your the current revision in Helix Core as a hex encoded value. This value will then be visible in Helix DAM as a preview image.

#### Arguments

None. The current open scene name will be used.

---

## update_dam_preview_blender.py


#### Usage

Intended to be run as a custom script in Blender. When clicked while you have a Blender scene open within a P4 client workspace it will take a screenshot of your current viewport and attach it to your the current revision in Helix Core as a hex encoded value. This value will then be visible in Helix DAM as a preview image.

#### Arguments

None. The current open scene name will be used.
