import matlab.engine
import os

class FSDA:
    def __init__(self, fsda_toolbox_path=None, shared_name='FSDA_Shared', matlab_engine_path=None):
        self.eng = self._connect_or_start(shared_name)

        if matlab_engine_path is None:
            matlab_engine_path = os.path.join(os.getcwd(), 'src', 'gateways', 'matlab_engine')

        self.eng.addpath(matlab_engine_path, nargout=0)

        if fsda_toolbox_path:
            self.eng.addpath(fsda_toolbox_path, nargout=0)

        self.wrapper = self.eng.FSDAEngine()

    def _connect_or_start(self, shared_name):
        try:
            # Pehle try karo — agar shared session chal rahi hai, usi se connect ho jao
            eng = matlab.engine.connect_matlab(shared_name)
            print(f"Connected to shared MATLAB session: {shared_name}")
            return eng
        except Exception:
            # Shared session nahi mili — apna khud ka background session start karo
            print("No shared session found — starting a new MATLAB engine...")
            return matlab.engine.start_matlab()

    def run(self, func_name, *args):
        return self.eng.feval('execute', self.wrapper, func_name, *args, nargout=1)

    def close(self):
        pass