{pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs.python310Packages; [
    pillow
    numpy
  ];
}
