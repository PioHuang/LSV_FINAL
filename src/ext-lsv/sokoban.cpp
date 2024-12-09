#include "base/abc/abc.h"
#include "base/main/main.h"
#include "base/main/mainInt.h"
#include "aig/aig/aig.h"
#include "iostream"
#include "set"
#include "queue"
#include "algorithm"
#include "sat/cnf/cnf.h"
#include "stdint.h"
#include <cstdlib>
#include <functional>
#include <unordered_set>
#include <thread> // For sleep
#include <chrono> // For time delays
#include "SokobanSolver.h"
using namespace std;

static int Sokoban_CommandSolve(Abc_Frame_t *pAbc, int argc, char **argv); // command function

void init(Abc_Frame_t *pAbc)
{
    Cmd_CommandAdd(pAbc, "LSV", "sokoban", Sokoban_CommandSolve, 0);
} // register this new command

void destroy(Abc_Frame_t *pAbc) {}

Abc_FrameInitializer_t frame_initializer = {init, destroy};

struct PackageRegistrationManager
{
    PackageRegistrationManager() { Abc_FrameAddInitializer(&frame_initializer); }
} lsvPackageRegistrationManager;
int Sokoban_CommandSolve(Abc_Frame_t *pAbc, int argc, char **argv)
{
    if (argc != 4)
    {
        cerr << "Usage: " << argv[0] << " <max step limit> <map file path> <run type>" << std::endl;
        return 1;
    }
    int maxStepLimit = atoi(argv[1]);
    const char *map = argv[2];
    int runType = atoi(argv[3]);

    if (runType == 1)
    {
        using namespace std::chrono;
        auto start = high_resolution_clock::now();
        for (int step = 1; step <= maxStepLimit; step++)
        {
            SokobanSolver Solver;
            Solver.setStepLimit(step);
            Solver.loadMap(map);
            sat_solver *pSat = sat_solver_new();
            Solver.AllConstraints();
            Solver.CnfWriter(pSat);

            // separate the constraints
            // increment steps, reuse previous clauses

            // Solver.debugger("Debug.txt");
            // cout << "Finished" << endl;

            vector<int> true_literals;
            // color code
            string black = "30";
            string red = "31";
            string green = "32"; // box color
            string yellow = "33";
            string blue = "34";

            int status = sat_solver_solve(pSat, nullptr, nullptr, 0, 0, 0, 0);
            // sat_solver_var_value(pSat, )
            if (status == l_True)
            {
                auto stop = high_resolution_clock::now();
                auto duration = duration_cast<seconds>(stop - start);
                cout << "Solution found at: " << step << " steps" << endl;
                cout << "BMC search duration: " << duration.count() << " seconds" << endl;

                string line;
                /*while (getline(f, line))
                {
                    stringstream ss(line);
                    int value;
                    while (ss >> value)
                        if (value > 0)
                            true_literals.push_back(value); // Add each value to the vector
                }
                f.close();

                cout << "Steps in action: " << endl;
                for (int t = 0; t <= step; t++)
                {
                    vector<vector<char>> visual(Solver.get_mapSize().first, vector<char>(Solver.get_mapSize().second, 'X'));
                    for (const auto &wall_coord : Solver.get_mapInfo()["Walls"])
                        visual[wall_coord.first][wall_coord.second] = 'W';
                    for (const auto &target_coord : Solver.get_mapInfo()["Targets"])
                        visual[target_coord.first][target_coord.second] = 'T';
                    for (auto val : true_literals)
                    {
                        Lit &lit = Solver.get_LitDictionary(val);
                        if (lit.get_t() == t)
                        {
                            if (lit.get_identity() == 1)
                                visual[lit.get_x()][lit.get_y()] = 'P';
                            else
                                visual[lit.get_x()][lit.get_y()] = 'B';
                        }
                    }
                    // print
                    for (int row = 0; row < Solver.get_mapSize().first; row++)
                    {
                        for (int col = 0; col < Solver.get_mapSize().second; col++)
                        {
                            switch (visual[row][col])
                            {
                            case 'B':
                                cout << "\033[" << green << "m" << visual[row][col] << "\033[0m" << " ";
                                break;
                            case 'P':
                                cout << visual[row][col] << " ";
                                break;
                            case 'T':
                                cout << "\033[" << red << "m" << visual[row][col] << "\033[0m" << " ";
                                break;
                            case 'W':
                                cout << "\033[" << yellow << "m" << visual[row][col] << "\033[0m" << " ";
                                break;
                            default:
                                cout << "\033[" << black << "m" << visual[row][col] << "\033[0m" << " ";
                                break;
                            }
                        }
                        cout << endl;
                    }
                    if (t < step)
                    {
                        cout.flush();
                        this_thread::sleep_for(chrono::seconds(1));
                        cout << "\033[" << Solver.get_mapSize().first << "A";
                    }
                }*/
                return 0;
            }
            sat_solver_delete(pSat);
        }
        cout << "Solution not found! Increase step max limit" << endl;
    }
    else // experimental features
    {
        SokobanSolver Solver;
        Solver.loadMap(map); // load first time
    }

    return 0;
}
