{
  description = "A print interface for the iFSR at TU Dresden";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (system: {
        default = pkgs.${system}.python311Packages.callPackage ./default.nix { };
      });
      hydraJobs = forAllSystems (system: {
        default = self.packages.${system}.default;
      });

      devShells = forAllSystems (system: {
        default = pkgs.${system}.mkShellNoCC {
          packages = with pkgs.${system}; [
            self.packages."x86_64-linux".default
          ];
        };
      });
    };
}
