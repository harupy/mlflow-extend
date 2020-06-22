# mypy: ignore-errors

import ast

from version import __version__

ERROR_CODE_LETTER = "B"


def _is_pytest_raises(context_expr):
    """
    Check if a context expression is `pytest.raises`.

    AST of `with pytest.raises(ValueError, match="match")` looks like:
    ==================================
    With(
        items=[
            withitem(
                context_expr=Call(
                    func=Attribute(
                        value=Name(id="pytest", ctx=Load()), attr="raises", ctx=Load()
                    ),
                    args=[Name(id="ValueError", ctx=Load())],
                    keywords=[
                        keyword(
                            arg="match",
                            value=Str(s="match"),
                        )
                    ],
                ),
                optional_vars=None,
            )
        ],
    )

    """
    return (
        isinstance(context_expr, ast.Call)
        and isinstance(context_expr.func, ast.Attribute)
        and context_expr.func.value.id == "pytest"
        and hasattr(context_expr.func, "attr")
        and context_expr.func.attr == "raises"
    )


def _get_num_args(call_stmt):
    """
    Get the number of arguments in a call statement.
    """
    return len(call_stmt.args) + len(call_stmt.keywords)


class BarePytestRaises:

    name = "bare_pytest_raises"
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree

    def run(self):
        for stmt in ast.walk(self.tree):
            if not isinstance(stmt, ast.With):
                continue

            context_expr = stmt.items[0].context_expr

            if not _is_pytest_raises(context_expr):
                continue

            if _get_num_args(context_expr) == 1:
                yield (
                    stmt.lineno,
                    stmt.col_offset,
                    f"{ERROR_CODE_LETTER}999: bare 'pytest.raises' is not allowed. specify 'match' argument",
                    type(self),
                )
