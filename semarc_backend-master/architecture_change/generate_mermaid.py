def json_to_mermaid(data):
    architecture_name = data.get("architecture_name", "Architecture")
    direction = data.get("direction", "top to bottom")
    mermaid_direction = "TD" if direction == "top to bottom" else "LR"

    components = data.get("components", [])
    connections = data.get("connections", [])

    mermaid = []
    # mermaid.append('```')
    mermaid.append(f"graph {mermaid_direction[:2].upper()}")
    mermaid.append(f'  subgraph Outer["{architecture_name}"]')
    mermaid.append(f"    direction LR\n")

    class_set = set()
    styles = []
    class_defs = {
        "green": "fill:#9f6,stroke:#333,stroke-width:2px;",
        "yellow": "fill:#f96,stroke:#333,stroke-width:2px;",
        "blue": "fill:#add8e6,stroke:#333,stroke-width:2px;",
        "red": "fill:#FF0000,stroke:#333,stroke-width:2px;"
    }
    all_elements = set()
    none_module= "none_module"
    layer_count = 1
    for comp in components:
        comp_name = comp["name"]
        elements = comp.get("elements", [])
        mermaid.append(f'    subgraph Layer{layer_count}["{comp_name}"]')
        mermaid.append("      direction TB")
        for el in elements:
            el_name = el["name"]
            if el_name in all_elements:
                # 添加一个dummy_node[""]
                # mermaid.append(f'     {comp_name}_{layer_count}["{comp_name}_{layer_count}"]')
                continue  # Skip duplicate elements
            all_elements.add(el_name)
            mermaid.append(f'      {el_name}["{el_name}"]')
            class_set.add((el_name, el["color"]))
        mermaid.append("    end")
        layer_count += 1

    mermaid.append("  end\n")

    # Add layer styles (fixed widths)
    for i in range(1, layer_count):
        mermaid.append(f"  style Layer{i} width:1200px;")
    mermaid.append("  \n")
    # Add node classes
    for node, color in class_set:
        mermaid.append(f"  class {node} {color};")
    mermaid.append("  \n")
    # Add classDefs
    for color, style_str in class_defs.items():
        mermaid.append(f"  classDef {color} {style_str}")
    mermaid.append("  \n")
    mermaid.append("   classDef blackText fill:#fff,stroke:#333,stroke-width:2px,color:#000;")
    mermaid.append("  class * defaultTextColor;")
    mermaid.append("  \n")
    # Add connections
    # mermaid.append('```')

    return "\n".join(mermaid)
