{
  description = "Computed Busy Beaver gauge";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        mm-tm = pkgs.fetchFromGitHub {
          owner = "sorear";
          repo = "metamath-turing-machines";
          rev = "530d5450cbf0fe7d0d104ec0f0ab037857e8a49c";
          sha256 = "sha256-k3QzWkBrE3/06rqCcEOvOfxHjcGrIB7hXHPMc9e/vlw=";
        };
        # XXX pypy doesn't work with pyparsing?
        py = pkgs.python3.withPackages (ps: [ ps.pyparsing ]);
        bb-gauge = pkgs.stdenv.mkDerivation {
          name = "bb-gauge";
          version = "0.0.1";

          src = ./.;

          buildInputs = with pkgs; [
            py jq
            mdbook mdbook-linkcheck
            # mdbook-graphviz
          ];

          buildPhase = ''
            for nql in $(<nql.json jq -r 'keys | join(" ")'); do
              states=$(${py}/bin/python3 ${mm-tm}/nqlaconic.py --print-tm ${mm-tm}/$nql | wc -l)
              echo "$nql | $states" >> src/turing-steps.md
            done
            mdbook build
          '';

          installPhase = ''
            mkdir -p $out/share/
            cp -r book/html/* $out/share/
          '';
        };
      in {
        packages.default = bb-gauge;
        devShells.default = pkgs.mkShell {
          name = "bb-gauge-env";
          packages = bb-gauge.buildInputs;
        };
      }
    );
}
