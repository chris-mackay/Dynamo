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

