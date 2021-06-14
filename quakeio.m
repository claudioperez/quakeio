function GroundMotion = quakeio(varargin)
[status, output] = system(strjoin({'quakeio', strjoin(varargin)}));
if strcmp(varargin{1},"-h") || strcmp(varargin{1},"--help")
  output
else
  GroundMotion = jsondecode(output);
end
end
