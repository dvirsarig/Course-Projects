#include "RecommendationSystemLoader.h"
std::unique_ptr<RecommendationSystem>
    RecommendationSystemLoader::create_rs_from_movies
    (const std::string &movies_file_path) noexcept (false){
  std::unique_ptr<RecommendationSystem> system =
      std::make_unique<RecommendationSystem>();
  std::ifstream file(movies_file_path);
  if (!file.is_open()) {
    throw std::runtime_error("Can't open the file.");
  }
  std::string line;
  while (std::getline(file,line)) {
    std::istringstream iss(line);
    std::string name;
    int year;
    double feature;
    std::string movie_name_and_year;
    if (!(iss >> movie_name_and_year)) {
      throw std::runtime_error("Error reading movie name and year.");
    }
    // Find the position of the hyphen
    size_t hyphen_pos = movie_name_and_year.find(YEAR_SEPARATOR);
    if (hyphen_pos != std::string::npos){
      // Extract the movie name and year based on the hyphen position
      name = movie_name_and_year.substr (0, hyphen_pos);
      std::string year_str = movie_name_and_year.substr (hyphen_pos + 1);
      // Convert the year string to an integer
      year = std::stoi (year_str);
    }
    else {
      throw::std::runtime_error("File is not with valid information.");
    }
    // Read and process ratings
    std::vector<double> features_vec;
    while (iss >> feature) {
      if (feature > MAX_FEATURE_VALUE || feature < MIN_FEATURE_VALUE){
        throw::std::runtime_error("File is not with valid information.");
      }
      features_vec.push_back (feature);
    }
    system->add_movie (name, year, features_vec);
  }
  file.close();
  return system;
}
