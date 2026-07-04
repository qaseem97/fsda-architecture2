classdef FSDAEngine < handle
    methods
        function out = execute(obj, funcName, varargin)
            try
                funcHandle = str2func(funcName);
                out = funcHandle(varargin{:});
            catch ME
                out = struct('status', 'error', 'message', ME.message);
            end
        end

        function out = ping(obj, message)
            out = struct('status', 'success', 'response', strcat('MATLAB received: ', message));
        end
    end
end