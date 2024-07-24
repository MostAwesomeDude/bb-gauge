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
        ghc = pkgs.haskellPackages.ghcWithPackages (ps: [ ps.dlist ]);
        ait = pkgs.stdenv.mkDerivation {
          name = "ait";
          version = "2024";

          src = pkgs.fetchFromGitHub {
            owner = "tromp";
            repo = "AIT";
            rev = "c4423db370320179342b8dd2ea8a484b7a127246";
            sha256 = "sha256-3wvWQjk9W8FIb4UUVQeStOhTnYcb+DikmDxQPt9Ffgs=";
          };

          buildInputs = [ ghc ];

          buildPhase = ''
            make blc
          '';

          installPhase = ''
            mkdir -p $out/bin/
            cp blc $out/bin/
          '';
        };
        perl = pkgs.perl.withPackages (ps: [ ps.DataDumper ]);
        bfmacro = pkgs.stdenv.mkDerivation {
          name = "bfmacro";
          version = "2005";

          src = builtins.fetchurl {
            url = "https://www.cs.tufts.edu/~couch/bfmacro/bfmacro/bfmacro";
            sha256 = "0dwlh3h58zv4slvv6cana6vgr9mgwln8y2227vj7r1n20agd3h3g";
          };

          dontUnpack = true;

          installPhase = ''
            mkdir -p $out/bin/
            echo "#!${perl}/bin/perl" | cat - $src > $out/bin/bfmacro
            chmod +x $out/bin/bfmacro
          '';

          meta.license = pkgs.lib.licenses.gpl2Plus;
        };
        # XXX pypy doesn't work with pyparsing?
        py = pkgs.python3.withPackages (ps: [ ps.pyparsing ]);
        bb-gauge = pkgs.stdenv.mkDerivation {
          name = "bb-gauge";
          version = "0.0.1";

          src = ./.;

          buildInputs = with pkgs; [
            py jq ait bfmacro
            mdbook mdbook-linkcheck
            # mdbook-graphviz
          ];

          buildPhase = ''
            for lam in $(<blc.json jq -r 'keys | join(" ")'); do
              len=$(${ait}/bin/blc size ${ait.src}/fast_growing_and_conjectures/$lam)
              echo "$lam | $len" >> src/blc-length.md
            done
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
