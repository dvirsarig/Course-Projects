#include "UsersLoader.h"

std::vector<std::pair<std::string, int>> all_movies(std::string& names)
noexcept(false){
  // This function take one line of names-years of the movies and insert
  // them as pair to a vector, if success return thr vector.
  std::istringstream iss(names);
  std::string full_name; //Name-Year
  std::vector<std::pair<std::string, int>> movies_name_and_year; //New vector
  while (std::getline(iss, full_name, ' ')){
    // Process each name (add to the vector)
    std::string name;
    int year;
    size_t hyphen_pos = full_name.find (YEAR_SEPARATOR);
    if (hyphen_pos != std::string::npos){
      // Extract the movie name and year based on the hyphen position.
      name = full_name.substr (0, hyphen_pos);
      std::string year_str = full_name.substr (hyphen_pos + 1);
      year = std::stoi (year_str); // Convert the year string to an integer.
      std::pair<std::string, int> new_pair = std::make_pair (name, year);
      movies_name_and_year.push_back (new_pair); //Add the movie to the vector.
    }
    else { // If something wrong with the name throw exception.
      throw::std::runtime_error("File is not with valid information.");
    }
  }
  return movies_name_and_year;
}

std::vector<User> UsersLoader::create_users(const std::string& users_file_path,
                                      std::unique_ptr<RecommendationSystem>rs)
                                      noexcept(false){
  // Move the system from unique to public.
  std::shared_ptr<RecommendationSystem> shared_sys = std::move(rs);
  // **Initialize all the values that needed** //
  std::vector<User> users; // The result.
  std::ifstream file(users_file_path); // Stream of the file.
  std::string user_name; // Catch users names
  std::vector<std::pair<std::string, int>> movies_name_and_year; //Keep
  // all the names of the movies by order.
  std::string line; // Catch the first line of the names of the movies.
  std::string rank_str; // To catch the rank of the user of each movie.
  if (!file.is_open()) { // Check if the file is valid.
    throw std::runtime_error("Can't open the file.");
  }
  std::getline (file, line); //Get first line and create vector of all
  // movies name by name and year.
  movies_name_and_year = all_movies (line);
  while (std::getline (file, line)) {
    std::istringstream iss(line);
    int index = 0; // Update the cur movie in the table.
    if (!(iss >> user_name)) {
      throw std::runtime_error("Error reading movie name and year.");
    }
    rank_map user_ranks(1, &sp_movie_hash, &sp_movie_equal); //Map of ranks.
    while (iss >> rank_str) {
      if (rank_str == "NA"){
        index++;
        continue;
      }
      double rank = std::stoi (rank_str);
      if (rank > MAX_RANK_VALUE || rank < MIN_RANK_VALUE){ // Check limits.
        throw::std::runtime_error("File is not with valid information.");
      }
      sp_movie movie = shared_sys->get_movie(movies_name_and_year[index].first,
                                   movies_name_and_year[index].second);
      user_ranks.insert ({movie, rank});
      index++; // Continue to the next movie on table.
    }
    // Clear the rest of the line by reading characters.
    User new_user(user_name, user_ranks, shared_sys);
    users.push_back (new_user);
  }
  file.close();
  return users;
}
