{
  pkgs ? import <nixpkgs> { },
}:

let
  pythonEnv = pkgs.python3.withPackages (
    ps: with ps; [
      requests
      basemap
    ]
  );
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
  ];
}
