from directed_acyclic_graph import DAG

dag = DAG()
dag.add_courses_from_json("courses.json")

if dag.is_dag():
    divisions = dag.topological_division()

    # Print the divisions
    for i, division in enumerate(divisions):
        print(f"Level {i + 1}: {[course.course_name for course in division]}")
else:
    print("The graph is not a DAG.")
