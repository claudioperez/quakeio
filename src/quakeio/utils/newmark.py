# import anon
import anabel
import anabel.backend as anp

try:
    from jax import jit
except ModuleNotFoundError:
    def jit(x):
        return x


@anabel.template.template(dim="shape", order=0, main="step", origin="origin")
def linear_accel_scalar(
    df, dt, *, mass, damp, beta=1 / 4, gamma=1 / 2, tol=1e-6, initial=(0.0, 0.0, 0.0)
):
    """Generate a 1D acceleration-driven Newmark integral.

    This function generates a Newmark integral from a
    zero-order map, `f`, and two matrices `mass` and `damp`.
    It was adaped from accel_no1 to return only displacements.

    Parameters
    ----------

    Studies
    -------

    created 2021-06-14
    """
    stif = df
    fshape = [[0, 0]]
    shape = (1, (fshape[0], fshape[0], fshape[0]))
    state = {
        "u": 0.0,
        "v": 0.0,
        "a": 0.0,
    }

    origin = 0.0, 0, state

    C1 = 1 / (beta * dt ** 2) * mass + gamma / (beta * dt) * damp
    C2 = 1 / (beta * dt) * mass + (gamma / beta - 1) * damp
    C3 = (1 / (beta * 2) - 1) * mass + dt * (gamma / (2 * beta) - 1) * damp

    @jit
    def step(state, ds, params={}, **kwds):
        u0, du0, ddu0 = state["u"], state["v"], state["a"]
        p_hat = mass * ds + C1 * u0 + C2 * du0 + C3 * ddu0
        # Initial evaluation
        fu0 = stif * u0
        res = p_hat - fu0 - C1 * u0
        Du = res / (stif + C1)
        u = u0 + Du

        du = (
            gamma / (beta * dt) * (u - u0)
            + (1 - gamma / beta) * du0
            + dt * (1 - gamma / (2 * beta)) * ddu0
        )
        ddu = (
            1 / (beta * dt ** 2) * (u - u0)
            - 1 / (beta * dt) * du0
            - (1 / (2 * beta) - 1) * ddu0
        )
        return {"u": u, "v": du, "a": ddu}, ddu

    return locals()


@anabel.template.template(dim="shape", order=0, main="step", origin="origin")
def linear_accel_vector(
    df, dt, *, mass, damp, beta=1 / 4, gamma=1 / 2, tol=1e-6, initial=None
):
    """Generate a 1D acceleration-driven Newmark integral.

    This function generates a Newmark integral from a
    zero-order map, `f`, and two matrices `mass` and `damp`.
    It was adaped from accel_no1 to return only displacements.

    Parameters
    ----------

    Studies
    -------

    created 2021-06-14
    """
    norm = anp.linalg.norm
    try:
        fshape = len(df)
    except TypeError:
        fshape = [[0, 0]]
    shape = (1, (fshape[0], fshape[0], fshape[0]))
    state = {
        "u": anp.zeros((1, 1)),
        "v": anp.zeros((1, 1)),
        "a": anp.zeros((1, 1)),
    }
    if initial is None:
        initial = anp.zeros((3, *fshape[0]))

    origin = 0.0, anp.zeros((1, 1)), state

    if isinstance(df, float):
        K_matrix = anp.array([[df]])
        mass = anp.array([[mass]])
        damp = anp.array([[damp]])

    C1 = 1 / (beta * dt ** 2) * mass + gamma / (beta * dt) * damp
    C2 = 1 / (beta * dt) * mass + (gamma / beta - 1) * damp
    C3 = (1 / (beta * 2) - 1) * mass + dt * (gamma / (2 * beta) - 1) * damp

    def step(ds, x0, state=state, params={}, **kwds):
        u0 = x0
        u0, du0, ddu0 = state["u"], state["v"], state["a"]
        p_hat = mass * ds + C1 @ u0 + C2 @ du0 + C3 @ ddu0
        # Initial evaluation
        fu0 = K_matrix @ u0
        res = p_hat - fu0 - C1 @ u0
        Du = anp.linalg.solve(K_matrix + C1, res)
        u = u0 + Du

        du = (
            gamma / (beta * dt) * (u - u0)
            + (1 - gamma / beta) * du0
            + dt * (1 - gamma / (2 * beta)) * ddu0
        )
        ddu = (
            1 / (beta * dt ** 2) * (u - u0)
            - 1 / (beta * dt) * du0
            - (1 / (2 * beta) - 1) * ddu0
        )
        return u, {"u": u, "v": du, "a": ddu}

    return locals()
