import sys

DEFAULT_EXCLUDED_FUNCTIONS = {
    "__init__",
    "__new__",
    "__repr__",
    "__str__",
    "<genexpr>",
    "<listcomp>",
    "<dictcomp>",
    "<setcomp>",
    "<lambda>",
}


class FunctionTracker:
    """Suit les fonctions exécutées et leurs relations hiérarchiques."""

    def __init__(
        self,
        root_frame=None,
        included_modules=(),
        excluded_modules=(),
        excluded_functions=None,
    ):
        self.root_frame = root_frame
        self.included_modules = tuple(included_modules or ())
        self.excluded_modules = tuple(excluded_modules or ())

        self.excluded_functions = (
            set(excluded_functions)
            if excluded_functions is not None
            else DEFAULT_EXCLUDED_FUNCTIONS.copy()
        )

        self.steps = []
        self.tracked_frames = {}

        self.original_exception = None
        self.original_exception_frame = None
        self.previous_trace = None

    def should_track(self, frame):
        """Détermine si une fonction doit être suivie."""

        # La fonction directement appelée par le décorateur
        # constitue la racine du suivi.
        if frame.f_back is self.root_frame:
            return True

        module = frame.f_globals.get("__name__", "")
        function_name = frame.f_code.co_name

        if frame is self.root_frame:
            return False

        if self.included_modules and not any(
            module.startswith(prefix) for prefix in self.included_modules
        ):
            return False

        if any(module.startswith(prefix) for prefix in self.excluded_modules):
            return False

        return function_name not in self.excluded_functions

    def _get_parent_id(self, frame):
        """Recherche le parent suivi le plus proche."""

        parent = frame.f_back

        while parent is not None:
            state = self.tracked_frames.get(id(parent))

            if state is not None:
                return state["step_index"]

            if parent is self.root_frame:
                break

            parent = parent.f_back

        return None

    def trace_call(self, frame):
        """Enregistre l'appel d'une fonction."""

        if not self.should_track(frame):
            return

        frame_id = id(frame)
        step_index = len(self.steps)
        parent_id = self._get_parent_id(frame)

        state = {
            "name": frame.f_code.co_name,
            "step_index": step_index,
            "parent_id": parent_id,
        }

        self.tracked_frames[frame_id] = state

        self.steps.append(
            {
                "name": frame.f_code.co_name,
                "success": None,
                "error": None,
                "parent_id": parent_id,
            }
        )

    def trace_exception(self, frame, exception):
        """Enregistre la première origine d'une exception."""

        if self.original_exception is not None:
            return

        self.original_exception = exception
        self.original_exception_frame = frame

    def trace_return(self, frame):
        """Finalise une étape suivie."""

        frame_id = id(frame)
        state = self.tracked_frames.get(frame_id)

        if state is None:
            return

        failed = (
            self.original_exception is not None
            and frame is self.original_exception_frame
        )

        self.steps[state["step_index"]] = {
            "name": state["name"],
            "success": not failed,
            "error": (str(self.original_exception) if failed else None),
            "parent_id": state["parent_id"],
        }

        self.tracked_frames.pop(frame_id, None)

    def trace(self, frame, event, arg):
        """Point d'entrée du traceur Python."""

        if event == "call":
            self.trace_call(frame)

        elif event == "exception":
            if id(frame) in self.tracked_frames:
                self.trace_exception(frame, arg[1])

        elif event == "return":
            self.trace_return(frame)

        return self.trace

    def get_steps(self, completed_only=False):
        """Retourne les étapes enregistrées."""

        steps = self.steps

        if completed_only:
            steps = [step for step in steps if step["success"] is not None]

        return tuple(steps)

    def start(self):
        """Active le suivi."""

        if self.previous_trace is not None:
            raise RuntimeError("Le tracker est déjà démarré.")

        self.previous_trace = sys.gettrace()
        sys.settrace(self.trace)

    def stop(self):
        """Arrête le suivi et restaure le traceur précédent."""

        if self.previous_trace is None:
            return

        sys.settrace(self.previous_trace)
        self.previous_trace = None
