if ~matlab.engine.isEngineShared
    matlab.engine.shareEngine('FSDA_Shared');
    disp('MATLAB Engine shared successfully as FSDA_Shared');
else
    disp('Engine already shared.');
end