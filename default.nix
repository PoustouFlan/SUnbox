let
  nixpkgs = import <nixpkgs> { };
in
  python3.pkgs.buildPythonApplication {
    pname = "sbox-your-mom";
    version = "1.0.0";

    src = nixpkgs.fetchgit {
      url = "https://github.com/PoustouFlan/SBoxYourMom";
      rev = "66f39c0b78f9bb4085c98b2847aeab5e6e0d92c2";
      hash = "sha256-NX/sX7ZLQPvB/61fbaku2wWIpCDwTc+k2ohBDyTPuNg=";
    };

    propagatedBuildInputs = with python3.pkgs; [
      pillow
      numpy
    ];

    pythonImportsCheck = [
      "sboxyourmom"
    ];
}
