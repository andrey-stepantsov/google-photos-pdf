{
  description = "Convert Google Photos ZIP exports to a single PDF";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python311;
        pythonPackages = python.pkgs;
      in
      {
        packages.default = pythonPackages.buildPythonApplication {
          pname = "google-photos-to-pdf";
          version = "0.1.8";
          format = "other";

          src = ./.;

          propagatedBuildInputs = with pythonPackages; [
            pillow
            pillow-heif
            img2pdf
            tqdm
          ];

          # No build phase needed - we're just installing a script
          dontBuild = true;

          installPhase = ''
            mkdir -p $out/bin
            cp main.py $out/bin/google-photos-to-pdf
            chmod +x $out/bin/google-photos-to-pdf
          '';

          meta = with pkgs.lib; {
            description = "Convert Google Photos ZIP exports to a single PDF";
            homepage = "https://github.com/andrey-stepantsov/google-photos-pdf";
            license = licenses.mit;
            maintainers = [ ];
            mainProgram = "google-photos-to-pdf";
          };
        };

        # Alias for backwards compatibility
        defaultPackage = self.packages.${system}.default;

        # Development shell with all dependencies
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pythonPackages.pillow
            pythonPackages.pillow-heif
            pythonPackages.img2pdf
            pythonPackages.tqdm
            pythonPackages.pytest
          ];
        };
      }
    );
}
