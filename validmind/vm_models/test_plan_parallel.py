def run_test_plan(test_plan_id, config, context, send=True):
    """
    Runs a test plan by its ID.
    """
    from ..test_plans import get_by_name

    test_plan = get_by_name(test_plan_id)
    print("running test plan", test_plan_id)
    test_plan_instance = test_plan(
        config=config,
        test_context=context,
    )
    test_plan_instance.run(render_summary=False, send=send)
    print("finished running test plan", test_plan_id)

    return test_plan_instance
