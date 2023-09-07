# Copyright © 2023 ValidMind Inc. All rights reserved.
non_test_content_block_html = """
<div
  class="lm-Widget p-Widget jupyter-widget-Collapse-header"
  style="padding: 6px; padding-left: 33px; font-size: 14px"
>
  <span>{content_type} Block: '{content_id}'</i></span>
</div>
"""

test_content_block_html = """
<div>
  <h2>{title}</h2>
  {description}
</div>
<h5 class="vm_required_context">
  Required Inputs: <span style="font-size: 13px"><i>{required_inputs}</i></span>
</h5>
<table class="vm_params_table" style="display: {table_display};">
    <tr>
        <th>Parameter</th>
        <th>Default Value</th>
    </tr>
    {params_table}
</table>

<style>
h5.vm_required_context {{
    margin-top: 25px;
}}
table.vm_params_table {{
  margin-top: 20px;
  width: 300px;
  border-collapse: collapse;
}}
table.vm_params_table td, table.vm_params_table th {{
  text-align: right;
}}
table.vm_params_table td:first-child, table.vm_params_table th:first-child {{
  text-align: left;
}}
table.vm_params_table tr:nth-child(odd) {{
  background-color: #f2f2f2;
}}
table.vm_params_table tr:hover {{
  background-color: #ddd;
}}
table.vm_params_table td, table.vm_params_table th {{
  padding: 5px;
  border: .8px solid #ddd;
}}
</style>
"""

failed_content_block_html = """
<div
  class="lm-Widget p-Widget jupyter-widget-Collapse-header"
  style="padding: 6px; padding-left: 13px; font-size: 14px;"
>
  <span>❌ &nbsp;&nbsp;Failed to load test: '{test_id}'</span>
</div>
"""
