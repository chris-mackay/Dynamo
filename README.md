# Dynamo
A collection of Revit Dynamo scripts

## Air Terminal Flow Totals

* Collects all the air terminals in a Revit project and totals their `Flow` based on `System Classification`.
* Expand the list of systems to calculate by adding items to `List Create`.

![air_terminals](air_terminal_totals.png?raw=true "air_terminals")

### Python code

```python
import clr
clr.AddReference('RevitNodes')

elements = IN[0]
systems = IN[1]
totals = []
	
for i in range(len(systems)):
	
	total = 0
	for e in elements:
		system = e.GetParameterValueByName("System Classification")
		airflow = e.GetParameterValueByName("Flow")
	
		if system == systems[i]: total += airflow
	
	totals.append(total)

OUT = totals
```

## Create Sheet Set

* Create a sheet set based on a revision description
* `Sheets.Revisions`, `Revision Properties`, and `ViewSets.ByViewsName` are apart of the [archi-labs.net](https://archi-lab.net/) package developed by [https://github.com/ksobon](https://github.com/ksobon)

![create_sheet_set](create_sheet_set.png?raw=true "create_sheet_set")
