function GroundMotion = quakeIO(varargin)
    python = 'python';
    if strcmp(varargin{1},"install")
        [status, output] = system( ...
            [python ' -m pip install --upgrade pip'], '-echo'...
        );
        [status, output] = system( ...
            [python ' -m pip install' ...
            ' --no-warn-script-location --upgrade quakeio'], '-echo'...
        );
        return
    end
    [status, output] = system(strjoin({'python -m quakeio', strjoin(varargin)}));
    if strcmp(varargin{1},"-h") || strcmp(varargin{1},"--help")
      output
    elseif ~status
      GroundMotion = jsondecode(output);
    else
      status
      output
    end
end
