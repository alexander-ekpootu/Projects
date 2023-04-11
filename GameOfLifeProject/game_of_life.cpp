#include <iostream>
#include <fstream>
#include <set>
#include <unistd.h>
#include <cstdlib>

using namespace std;

class GameOfLife {
public:
    GameOfLife() = default;

    void set_alive(uint32_t row, uint32_t col) {
        alive_cells.insert(make_pair(row, col));
    }

    void next_generation() {
        set<pair<uint32_t, uint32_t>> new_alive_cells;
        set<pair<uint32_t, uint32_t>> checked_cells;

        for (const auto& cell : alive_cells) {
            for (int i = -1; i <= 1; ++i) {
                for (int j = -1; j <= 1; ++j) {
                    uint32_t newRow = cell.first + i;
                    uint32_t newCol = cell.second + j;
                    if (checked_cells.count(make_pair(newRow, newCol)) == 0) {
                        int live_neighbors = count_live_neighbors(newRow, newCol);
                        if (alive_cells.count(make_pair(newRow, newCol))) {
                            if (live_neighbors == 2 || live_neighbors == 3) {
                                new_alive_cells.insert(make_pair(newRow, newCol));
                            }
                        } else {
                            if (live_neighbors == 3) {
                                new_alive_cells.insert(make_pair(newRow, newCol));
                            }
                        }
                        checked_cells.insert(make_pair(newRow, newCol));
                    }
                }
            }
        }
        alive_cells = new_alive_cells;
    }

    void display(int rows, int cols) {
        uint32_t minRow = UINT32_MAX;
        uint32_t maxRow = 0;
        uint32_t minCol = UINT32_MAX;
        uint32_t maxCol = 0;
        for (const auto& cell : alive_cells) {
            minRow = min(minRow, cell.first);
            maxRow = max(maxRow, cell.first);
            minCol = min(minCol, cell.second);
            maxCol = max(maxCol, cell.second);
        }
        uint32_t numRows = maxRow - minRow + 1;
        uint32_t numCols = maxCol - minCol + 1;
        uint32_t rowOffset = (rows - numRows) / 2;
        uint32_t colOffset = (cols - numCols) / 2;
        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (alive_cells.count(make_pair(row + minRow - rowOffset, col + minCol - colOffset))) {
                    cout << '.';
                } else {
                    cout << ' ';
                }
                cout << ' ';
            }
            cout << endl;
        }
    }

    void save_to_file(const string& filename) {
        ofstream outfile(filename);
        for (const auto& cell : alive_cells) {
            outfile << cell.first << " " << cell.second << endl;
        }
        outfile.close();
    }

    void load_from_file(const string& filename) {
        alive_cells.clear();
        ifstream infile(filename);
        uint32_t row, col;
        while (infile >> row >> col) {
            set_alive(row, col);
        }
        infile.close();
    }    

private:
    int count_live_neighbors(uint32_t row, uint32_t col) {
        int count = 0;
        for (int i = -1; i <= 1; ++i) {
            for (int j = -1; j <= 1; ++j) {
                if (i == 0 && j == 0) continue;
                uint32_t newRow = row + i;
                uint32_t newCol = col + j;
                count += alive_cells.count(make_pair(newRow, newCol)) ? 1 : 0;
            }
        }
        return count;
    }

    set<pair<uint32_t, uint32_t>> alive_cells;
};

int main() {
    GameOfLife game;

    // Load the initial pattern from a file
    game.load_from_file("initial_pattern.txt");

    int display_rows = 20;
    int display_cols = 20;
    int num_generations = 50; // Set the number of generations

    for (int generation = 0; generation < num_generations; ++generation) {
        system("clear");
        game.display(display_rows, display_cols);
        game.next_generation();
        usleep(100000);

        // Save the universe to a file
        game.save_to_file("current_universe.txt");
    }

    return 0;
}