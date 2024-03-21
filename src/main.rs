// Import required libraries
use std::env;
use std::fs::{File, create_dir_all};
use std::process;
use std::path::Path;
use bio::io::fastq::{Reader as FqReader, Writer as FqWriter};
use itertools::izip;

const OUTPUT_DIR: &str = "./filtered_fastq/";

fn create_directory(dir: &str) -> Result<(), Box<dyn std::error::Error>> {
  let dir_path = Path::new(dir);
  Ok(create_dir_all(dir_path)?)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
  let args: Vec<String> = env::args().collect();
  if args.len() < 4 {
      eprintln!("Usage: {} <input_file_1> <input_file_2> <output_prefix>", args[0]);
      process::exit(1);
  }

  let fq_r1 = &args[1];
  let fq_r2 = &args[2];
  let output_prefix = &args[3];

  create_directory(OUTPUT_DIR)?;

  let start_time = std::time::Instant::now();

  let r1_handle = File::open(fq_r1)?;
  let r2_handle = File::open(fq_r2)?;

  let r1_reader = FqReader::new(r1_handle);
  let r2_reader = FqReader::new(r2_handle);

  let mut r1_writer = FqWriter::new(File::create(format!("{}_filtered.R1.fastq", output_prefix)).unwrap());
  let mut r2_writer = FqWriter::new(File::create(format!("{}_filtered.R2.fastq", output_prefix)).unwrap());

  for (record1, record2) in izip!(r1_reader.records(), r2_reader.records()) {
      match (record1, record2) {
          (Ok(record1), Ok(record2)) => {
              if (record1.seq().len() == record1.qual().len()) & (record2.seq().len() == record2.qual().len()) {
                 r1_writer.write_record(&record1)?;
                 r2_writer.write_record(&record2)?;
              }
          },
          _ => {},
      };
  }

  println!("Filtering completed in {} seconds.", start_time.elapsed().as_secs_f64());

  Ok(())
}