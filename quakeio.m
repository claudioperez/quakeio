function GroundMotion = quakeio(varargin)
[status, output] = system(strjoin({'quakeio', strjoin(varargin)}));
GroundMotion = jsondecode(output);
end
