#include <TString.h>
#include "CLI11.hpp"

void makehistfromtracks(TString input, TString tree, TString folder);


int main(int argc, char** argv) {

    CLI::App app("make_hist_from_tracks", "Make kernel from a tracks file");
    app.option_defaults()->always_capture_default();

    TString base = "10pvs";
    app.add_option("base,--base", base);

    TString tree = "trks";
    app.add_option("tree,--tree", tree);

    TString folder = "../../dat";
    app.add_option("folder,--folder", folder);

    CLI11_PARSE(app, argc, argv);

    makehistfromtracks(base, tree, folder);
}
