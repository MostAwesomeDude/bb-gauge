{
  lib,
  stdenv,
  fetchzip,
  fetchurl,
  writeText,
  pkg-config,
  gnumake42,
  ocamlPackages_4_14,
  ncurses,
}@args:
let
  src = fetchzip {
    url = "https://github.com/coq/coq/archive/V8.20.1.zip";
    sha256 = "sha256-nRaLODPG4E3gUDzGrCK40vhl4+VhPyd+/fXFK/HC3Ig=";
  };
  version = "8.20.1";
  coq-version = "8.20.1";
  ocamlPackages = ocamlPackages_4_14;
  ocamlNativeBuildInputs = [
    ocamlPackages.ocaml
    ocamlPackages.findlib
    ocamlPackages.dune_3
  ];
  ocamlPropagatedBuildInputs = [ ocamlPackages.zarith ];
  self = stdenv.mkDerivation {
    pname = "coq";
    inherit version src;

    passthru = {
      inherit coq-version;
      inherit ocamlPackages ocamlNativeBuildInputs;
      inherit ocamlPropagatedBuildInputs;
      # For compatibility
      inherit (ocamlPackages)
        ocaml
        camlp5
        findlib
        num
        ;
      emacsBufferSetup = pkgs: ''
        ; Propagate coq paths to children
        (inherit-local-permanent coq-prog-name "${self}/bin/coqtop")
        (inherit-local-permanent coq-dependency-analyzer "${self}/bin/coqdep")
        (inherit-local-permanent coq-compiler "${self}/bin/coqc")
        ; If the coq-library path was already set, re-set it based on our current coq
        (when (fboundp 'get-coq-library-directory)
          (inherit-local-permanent coq-library-directory (get-coq-library-directory))
          (coq-prog-args))
        (mapc (lambda (arg)
          (when (file-directory-p (concat arg "/lib/coq/${coq-version}/user-contrib"))
            (setenv "COQPATH" (concat (getenv "COQPATH") ":" arg "/lib/coq/${coq-version}/user-contrib")))) '(${
              lib.concatStringsSep " " (map (pkg: "\"${pkg}\"") pkgs)
            }))
        ; TODO Abstract this pattern from here and nixBufferBuilders.withPackages!
        (defvar nixpkgs--coq-buffer-count 0)
        (when (eq nixpkgs--coq-buffer-count 0)
          (make-variable-buffer-local 'nixpkgs--is-nixpkgs-coq-buffer)
          (defun nixpkgs--coq-inherit (buf)
            (inherit-local-inherit-child buf)
            (with-current-buffer buf
              (setq nixpkgs--coq-buffer-count (1+ nixpkgs--coq-buffer-count))
              (add-hook 'kill-buffer-hook 'nixpkgs--decrement-coq-buffer-count nil t))
            buf)
          ; When generating a scomint buffer, do inherit-local inheritance and make it a nixpkgs-coq buffer
          (defun nixpkgs--around-scomint-make (orig &rest r)
            (if nixpkgs--is-nixpkgs-coq-buffer
                (progn
                  (advice-add 'get-buffer-create :filter-return #'nixpkgs--coq-inherit)
                  (apply orig r)
                  (advice-remove 'get-buffer-create #'nixpkgs--coq-inherit))
              (apply orig r)))
          (advice-add 'scomint-make :around #'nixpkgs--around-scomint-make)
          ; When we have no more coq buffers, tear down the buffer handling
          (defun nixpkgs--decrement-coq-buffer-count ()
            (setq nixpkgs--coq-buffer-count (1- nixpkgs--coq-buffer-count))
            (when (eq nixpkgs--coq-buffer-count 0)
              (advice-remove 'scomint-make #'nixpkgs--around-scomint-make)
              (fmakunbound 'nixpkgs--around-scomint-make)
              (fmakunbound 'nixpkgs--coq-inherit)
              (fmakunbound 'nixpkgs--decrement-coq-buffer-count))))
        (setq nixpkgs--coq-buffer-count (1+ nixpkgs--coq-buffer-count))
        (add-hook 'kill-buffer-hook 'nixpkgs--decrement-coq-buffer-count nil t)
        (setq nixpkgs--is-nixpkgs-coq-buffer t)
        (inherit-local 'nixpkgs--is-nixpkgs-coq-buffer)
      '';
    };

    nativeBuildInputs = [ pkg-config ] ++ ocamlNativeBuildInputs;
    buildInputs = [ ncurses ];

    propagatedBuildInputs = ocamlPropagatedBuildInputs
    ++ [ ocamlPackages.ocaml ];

    postPatch = ''
      UNAME=$(type -tp uname)
      RM=$(type -tp rm)
      substituteInPlace tools/beautify-archive --replace "/bin/rm" "$RM"
    '';

    setupHook = writeText "setupHook.sh" ''
      addCoqPath () {
        if test -d "''$1/lib/coq/${coq-version}/user-contrib"; then
          export COQPATH="''${COQPATH-}''${COQPATH:+:}''$1/lib/coq/${coq-version}/user-contrib/"
        fi
      }

      addEnvHooks "$targetOffset" addCoqPath
    '';

    preConfigure = ''
      patchShebangs dev/tools/
      configureFlagsArray=(-native-compiler yes)
    '';

    prefixKey = "-prefix ";

    buildFlags = [
      "revision"
      "coq"
    ];
    enableParallelBuilding = true;

    createFindlibDestdir = true;

    postInstall =
      let
        suffix = "-core";
      in
      ''
        ln -s $out/lib/coq${suffix} $OCAMLFIND_DESTDIR/coq${suffix}
        ln -s $out/lib/coqide-server $OCAMLFIND_DESTDIR/coqide-server
      '';

    meta = with lib; {
      description = "Coq proof assistant";
      longDescription = ''
        Coq is a formal proof management system.  It provides a formal language
        to write mathematical definitions, executable algorithms and theorems
        together with an environment for semi-interactive development of
        machine-checked proofs.
      '';
      homepage = "https://coq.inria.fr";
      license = licenses.lgpl21;
      branch = coq-version;
      platforms = platforms.unix;
    };
  };
in self.overrideAttrs (_: {
    buildPhase = ''
      runHook preBuild
      make dunestrap
      dune build -p coq-core,coq-stdlib,coqide-server -j $NIX_BUILD_CORES
      runHook postBuild
    '';
    installPhase = ''
      runHook preInstall
      dune install --prefix $out coq-core coq-stdlib coqide-server
      runHook postInstall
    '';
  })
