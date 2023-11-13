from directed_acyclic_graph import DAG

def generate_course_divisions():
    dag = DAG()
    dag.add_courses_from_json("courses.json")

    if dag.is_dag():
        return dag.topological_division()
    else:
        print("The graph is not a DAG.")
        return None
