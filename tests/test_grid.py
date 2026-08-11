from aoigrid import SpatialGrid

def test_insert_query():
    grid = SpatialGrid(cell_size=10.0)
    grid.insert("a", (5, 5))
    grid.insert("b", (50, 50))
    assert "a" in grid.query_radius((5, 5), 10)
    assert "b" not in grid.query_radius((5, 5), 10)

def test_3d():
    grid = SpatialGrid(cell_size=5.0, dimensions=3)
    grid.insert("x", (1, 1, 1))
    grid.insert("y", (100, 100, 100))
    assert "x" in grid.query_radius((1, 1, 1), 3)
    assert "y" not in grid.query_radius((1, 1, 1), 3)

def test_clear():
    grid = SpatialGrid(cell_size=10.0)
    grid.insert("a", (5, 5))
    grid.clear()
    assert len(grid) == 0
