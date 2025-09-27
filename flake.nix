{
  description = "Computed Busy Beaver gauge";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
    rpypkgs = {
      url = "github:rpypkgs/rpypkgs";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "flake-utils";
      };
    };
  };

  outputs = { self, nixpkgs, flake-utils, rpypkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        coq-bb5 = pkgs.stdenv.mkDerivation {
          name = "coq-bb5";
          version = "1.0.0";

          src = pkgs.fetchFromGitHub {
            owner = "ccz181078";
            repo = "Coq-BB5";
            rev = "b295161e830cfb0698e6eff667afce8917ca1423";
            sha256 = "sha256-O4TpmXUxryD20zF9+yCDKqUeNCH4Xe14i4urUiPok2E=";
          };

          nativeBuildInputs = [ pkgs.coq_8_20 ];

          buildPhase = ''
            make -C CoqBB5/BB2
            make -C CoqBB5/BB2x3
            make -C CoqBB5/BB2x4
            make -C CoqBB5/BB3
            make -C CoqBB5/BB4
            make -C BusyCoq
            make -C CoqBB5/BB5
          '';

          installPhase = ''
            mkdir $out/ -p
            touch $out/proof.success
          '';
        };
        mm-tm = pkgs.fetchFromGitHub {
          owner = "MostAwesomeDude";
          repo = "metamath-turing-machines";
          rev = "f88c4ee389e95f21e698c997bfa1e40a6bb04cb5";
          sha256 = "sha256-7ONKuPf9E1V2agZBPfCfweI6n8xF29W1WnB6MPy72W4=";
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

          src = pkgs.fetchurl {
            urls = [
              "https://www.cs.tufts.edu/~couch/bfmacro/bfmacro/bfmacro"
              "https://corbinsimpson.com/mirror/bfmacro"
            ];
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
        bf-bcl = builtins.fetchurl {
          url = "https://paste.debian.net/plain/1332858/";
          sha256 = "0yhqfsgdsa8vlkk7agmr2ri1vvdjmcp44vbclxg259q48chk6qnn";
        };
        bf-dbfi = builtins.fetchurl {
          url = "http://brainfuck.org/dbfi.b";
          sha256 = "19zixvz4axfcjyfss5hirahng5ksnrsmpdibacc5g6wgi10amii5";
        };
        bf-utm = builtins.fetchurl {
          url = "http://brainfuck.org/utm.b";
          sha256 = "1p7dk6fbn29rn9s35rkhcrggfg136dy5rkc89f0960al6ij7y5bx";
        };
        bf-meta = pkgs.stdenv.mkDerivation {
          name = "meta.bf";
          version = "2023";
          src = pkgs.fetchFromGitHub {
            owner = "bf-enterprise-solutions";
            repo = "meta.bf";
            rev = "e42de471a8434beb055e1590c259131c225eb423";
            sha256 = "sha256-iOB/1UMNiqQ8Hibjo/7B3HaQNiYdQFB5Gtr+DvCSkqE=";
          };
          nativeBuildInputs = [ pkgs.m4 ];
          installPhase = ''
            mkdir -p $out/share/
            cp meta.*.bf $out/share/
          '';
        };
        bf = rpypkgs.packages.${system}.bf;
        # XXX pypy doesn't work with pyparsing?
        py = pkgs.python3.withPackages (ps: [ ps.pyparsing ]);
        bb-gauge = pkgs.stdenv.mkDerivation {
          name = "bb-gauge";
          version = "0.0.1";

          src = ./.;

          nativeBuildInputs = with pkgs; [
            py jq ait bfmacro
            mdbook mdbook-linkcheck
          ];

          buildPhase = ''
            # Clean bfmacro.
            ${bfmacro}/bin/bfmacro -na bfm/stack.bfm bfm/laver.bfm \
              | sed '/^ *!/d' > bf/laver.b
            ${bfmacro}/bin/bfmacro -na bfm/stack.bfm bfm/erdos-lagarias.bfm \
              | sed '/^ *!/d' > bf/erdos-lagarias.b
            cp ${bf-bcl} bf/bcl.bf
            cp ${bf-dbfi} bf/dbfi.b
            cp ${bf-utm} bf/utm.b
            cp ${bf-meta}/share/meta.r.min.bf bf/meta.bf
            mkdir bf-clean/
            # Compress BF.
            for b in bf/*; do
              t="bf-clean/$(basename $b)"
              echo "Cleaning $b"
              ${bf}/bin/bf -o $b >$t
            done

            # Copy BLC to the correct locations.
            cp -r ${ait.src}/ait/ blc/ait/
            cp -r ${ait.src}/fast_growing_and_conjectures/ blc/fast_growing_and_conjectures/

            # Copy NQL to the correct locations.
            mkdir nql/
            cp ${mm-tm}/*.nql nql/
            cp ${mm-tm}/{nqlast,nqlgrammar,framework}.py .

            # Generate tables and diagrams.
            mkdir src/images/
            ${py}/bin/python3 gen.py turing.json src/turing.md src/images/turing.svg
            ${py}/bin/python3 gen.py brainfuck.json src/brainfuck-table.md src/images/brainfuck.svg
            ${py}/bin/python3 gen.py lambda.json src/lambda.md src/images/lambda.svg

            mdbook build
          '';

          installPhase = ''
            mkdir -p $out/share/images/
            cp -r book/html/* $out/share/

            mkdir -p $out/lib/
            cp -r bf/ bf-clean/ $out/lib/
          '';
        };
      in {
        packages = {
          inherit coq-bb5;
          default = bb-gauge;
        };
        devShells.default = pkgs.mkShell {
          name = "bb-gauge-env";
          packages = bb-gauge.buildInputs ++ [
            bf
            pkgs.python3Packages.pyflakes pkgs.jq
          ];
        };
      }
    );
}
