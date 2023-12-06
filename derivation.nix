{ lib
, fetchFromGitHub
, python3
}:

python3.pkgs.buildPythonApplication {
  pname = "sunbox";
  version = "1.0.0";

  src = ./.;

  propagatedBuildInputs = with python3.pkgs; [
    setuptools
    pillow
    numpy
  ];
}
