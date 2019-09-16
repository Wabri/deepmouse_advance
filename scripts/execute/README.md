
# Execute

# On linux

To use this script you must abilitate the source [file](/scripts/development_setup).

The script [run.sh](run.sh): Set up the virtual environment and activate it, install pip and requirements, run the package passed by argument, then deactivate and remove environment.

This script must be run on the root of the project and can takes multiple arguments:

```Bash
sh scripts/execute/run.sh <name_of_package> [<arguments>]
```

## Mouse recorder

Arguments:

- --username='<string_value>'
- --max_iterations=<integer_value>
- --point_per_file=<integer_value>
- --sleep_time=<float_value>

Example:

```Bash
sh scripts/execute/run.sh mouse_recorder \
			--username=Gabriele \
		 	--max_iterations=10 \
			--point_per_file=25 \
			--sleep_time=0.10
```

