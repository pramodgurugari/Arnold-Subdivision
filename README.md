🌟 Arnold Subdivision Tool for Autodesk Maya
Created by Pramod G | Version 1.2

![Arnold Subdivision](https://github.com/user-attachments/assets/575b30c9-d8af-43df-a9b1-2349088e8737)



https://github.com/user-attachments/assets/79e7f10c-b6be-4097-b83c-cee3c6b2ff0f




This is a custom UI tool for Autodesk Maya that enables non-destructive, artist-friendly subdivision control for Arnold renderer. Designed to work seamlessly across Maya versions, the tool allows artists to efficiently apply or auto-assign subdivision settings on selected meshes or the entire scene.

🎯 Key Features:
🔧 Subdivision Type Control
Choose between none, catclark, and linear modes directly in the UI.

🔁 Subdivision Iteration Level
Easily adjust iterations using an intuitive slider and spinbox (0–30 levels).

🧠 Smart Auto-Assignment
Automatically detects mesh face count and sets appropriate subdivision level for optimized performance and quality.

📌 Scope Flexibility
Choose to apply settings on:

Selected objects

All scene meshes

Auto mode (smart decision-making based on geometry complexity)

✅ Robust Attribute Handling
Checks and adds aiSubdivType and aiSubdivIterations if missing, ensuring compatibility with Arnold rendering pipeline.

💻 Compatibility:
✔ Arnold Render-compatible
✔ No external dependencies

💬 Summary:
This tool streamlines the process of managing Arnold's subdivision settings in Maya, giving artists full control or intelligent automation in heavy scenes. Whether you're optimizing render quality or tweaking settings per asset, this tool saves time while ensuring consistency and flexibility.

Feel free to fork, modify, or integrate it into your Maya pipeline!


🔧 Customizing Auto-Assign Logic
Note: You can modify the Auto Assign behavior to better suit your production needs by customizing the logic below:

python
Copy
Edit
----------------------------------------------------------
if auto_assign:
    face_count = cmds.polyEvaluate(obj, face=True)

    if face_count > 100000:
        level = 1  # Minimal subdivision for heavy meshes
    elif face_count > 10000:
        level = 2  # Moderate subdivision
    else:
        level = 3  # Higher quality for lightweight meshes
----------------------------------------------------------------
This logic determines the subdivision level based on the number of faces on each mesh. You can adjust the thresholds (100000, 10000) or the assigned levels (1, 2, 3) as needed for your specific project or rendering pipeline
